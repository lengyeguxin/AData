"""
定时任务调度器

功能：
- 间隔检查模式：每隔check_interval分钟检查是否需要拉取数据
- 如果任务正在运行 → 跳过（max_instances=1）
- 如果任务未运行 → 启动拉取
- 30分钟定时快照生成
- 1小时定时WAL checkpoint
- 异常处理和重试机制

优势：
- 避免长时间拉取导致定时任务被跳过
- 更灵活的调度机制
- 自动适应数据拉取时长变化
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from datetime import datetime, timedelta
from typing import Dict
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from src.core.logger import get_logger
from src.core.database import Database
from src.core.data_fetcher import DataFetcher
import yaml
import shutil


class DataScheduler:
    """数据定时任务调度器"""

    def __init__(self, config: Dict):
        """
        初始化调度器

        Args:
            config: 配置字典
        """
        self.config = config
        self.logger = get_logger(__name__)

        # 初始化组件
        db_path = 'database/adata.db'
        self.db = Database(db_path)
        self.fetcher = DataFetcher(db_path, config)

        # 创建后台调度器
        self.scheduler = BackgroundScheduler()

        # 从配置读取时间参数
        scheduler_config = config.get('scheduler', {})
        self.snapshot_interval = config.get('snapshot', {}).get('interval', 30)
        self.check_interval = config.get('fetch', {}).get('check_interval', 60)

        self.logger.info(f"调度器初始化完成")
        self.logger.info(f"数据拉取检查间隔: {self.check_interval}分钟")
        self.logger.info(f"快照间隔: {self.snapshot_interval}分钟")

    def start(self):
        """
        启动调度器

        添加所有定时任务并启动
        """
        self.logger.info("启动定时任务调度器...")

        # 1. 日线数据定时拉取任务（每天18:00）
        self.add_daily_fetch_job()

        # 2. 快照定时生成任务（每30分钟）
        self.add_snapshot_job()

        # 3. WAL checkpoint任务（每1小时）
        self.add_checkpoint_job()

        # 4. 启动调度器
        self.scheduler.start()
        self.logger.info("✓ 定时任务调度器已启动")

    def stop(self):
        """停止调度器"""
        self.logger.info("停止定时任务调度器...")
        self.scheduler.shutdown()
        self.logger.info("✓ 定时任务调度器已停止")

    def add_daily_fetch_job(self):
        """
        添加数据拉取定时任务（间隔检查模式）

        机制：每隔check_interval分钟检查一次
              - 如果任务正在运行 → 跳过（max_instances=1）
              - 如果任务未运行 → 启动拉取

        优势：避免长时间拉取导致定时任务被跳过
        """
        # 从配置读取检查间隔（分钟）
        check_interval = self.config.get('fetch', {}).get('check_interval', 60)

        # 创建interval触发器（每隔check_interval分钟检查一次）
        trigger = IntervalTrigger(minutes=check_interval)

        # 添加任务
        self.scheduler.add_job(
            self.fetch_daily_data,
            trigger,
            id='daily_fetch',
            name='数据拉取（间隔检查）',
            max_instances=1,  # 只允许一个实例运行
            misfire_grace_time=600  # 允许10分钟内的延迟执行
        )

        self.logger.info(f"✓ 已添加数据拉取任务: 每{check_interval}分钟检查一次")

    def add_snapshot_job(self):
        """
        添加快照定时生成任务

        时间：每30分钟（可配置）
        任务：生成数据库快照（两个位置）
        """
        # 创建interval触发器
        trigger = IntervalTrigger(minutes=self.snapshot_interval)

        # 添加任务
        self.scheduler.add_job(
            self.create_snapshot,
            trigger,
            id='snapshot',
            name='数据库快照',
            max_instances=1,
            misfire_grace_time=600  # 允许10分钟内的延迟执行
        )

        self.logger.info(f"✓ 已添加快照生成任务: 每{self.snapshot_interval}分钟")

    def add_checkpoint_job(self):
        """
        添加WAL checkpoint定时任务

        时间：每1小时
        任务：执行checkpoint，将WAL合并到主数据库文件
        """
        # 创建interval触发器（每1小时）
        trigger = IntervalTrigger(hours=1)

        # 添加任务
        self.scheduler.add_job(
            self.execute_checkpoint,
            trigger,
            id='checkpoint',
            name='WAL Checkpoint',
            max_instances=1,
            misfire_grace_time=300  # 允许5分钟内的延迟执行
        )

        self.logger.info(f"✓ 已添加checkpoint任务: 每1小时")

    def fetch_daily_data(self):
        """
        拉取数据任务（检查running状态）

        任务内容：
        - 检查DataFetcher.running状态
        - 如果running=True（任务正在运行）→ 跳过
        - 如果running=False（任务未运行）→ 启动拉取
        - 异常处理和日志记录
        """
        self.logger.info("=" * 80)
        self.logger.info("定时检查：是否需要拉取数据")
        self.logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 检查running状态
        from src.core.data_fetcher import DataFetcher

        if DataFetcher.running:
            self.logger.info("⚠️  数据拉取任务正在运行（running=True）→ 跳过本次触发")
            self.logger.info("=" * 80)
            return

        self.logger.info("✓ 数据拉取任务未运行（running=False）→ 启动拉取")
        self.logger.info("=" * 80)

        try:
            # 调用DataFetcher拉取数据
            self.fetcher.start()

            self.logger.info("✓ 数据拉取完成")

        except Exception as e:
            self.logger.error(f"✗ 数据拉取失败: {e}")
            # 发送通知（待实现）

        self.logger.info("=" * 80)

    def create_snapshot(self):
        """
        创建数据库快照任务

        任务内容：
        - 复制主数据库到两个快照位置
        - 异常处理和日志记录
        """
        self.logger.info("开始生成数据库快照...")

        try:
            # 主数据库路径
            main_db = 'database/adata.db'

            # 快照位置
            snapshot_locations = self.config.get('snapshot', {}).get('locations', [
                'database/adata_snapshot.db',
                '/home/my/claude-project/AiStock/database/adata_snapshot.db'
            ])

            # 复制快照到每个位置
            for snapshot_path in snapshot_locations:
                shutil.copy2(main_db, snapshot_path)
                self.logger.info(f"✓ 快照已保存: {snapshot_path}")

            self.logger.info(f"✓ 数据库快照生成完成（{len(snapshot_locations)}个位置）")

        except Exception as e:
            self.logger.error(f"✗ 快照生成失败: {e}")
            # 发送通知（待实现）

    def execute_checkpoint(self):
        """
        执行WAL checkpoint任务（检查running状态，避免冲突）

        任务内容：
        - 检查DataFetcher.running状态
        - 如果running=True（正在拉取）→ 跳过（每个表完成后自动checkpoint）
        - 如果running=False（任务未运行）→ 执行checkpoint
        - 将WAL合并到主数据库文件
        - 减少WAL文件大小
        """
        from src.core.data_fetcher import DataFetcher

        # 检查running状态（拉取中每个表会自动checkpoint，不需要调度器执行）
        if DataFetcher.running:
            self.logger.info("⚠️  数据正在拉取（running=True）→ 跳过checkpoint（表完成后自动执行）")
            return

        self.logger.info("开始执行checkpoint（数据拉取未运行）...")

        try:
            # 使用Database类的checkpoint方法
            db = Database('database/adata.db')
            success = db.checkpoint()
            db.close()

            if success:
                import os
                wal_size = os.path.getsize('database/adata.db.wal') / 1024.0 / 1024.0 if os.path.exists('database/adata.db.wal') else 0
                self.logger.info(f"✓ Checkpoint执行成功，WAL已合并（WAL大小: {wal_size:.2f}MB）")
            else:
                self.logger.warning("⚠️  Checkpoint执行失败")

        except Exception as e:
            self.logger.error(f"✗ Checkpoint执行失败: {e}")

    def get_jobs_status(self) -> Dict:
        """
        获取所有任务状态

        Returns:
            任务状态字典
        """
        jobs = self.scheduler.get_jobs()

        status = {}
        for job in jobs:
            status[job.id] = {
                'name': job.name,
                'next_run_time': str(job.next_run_time),
                'trigger': str(job.trigger),
                'pending': job.pending
            }

        return status


def main():
    """
    测试调度器启动

    启动后查看定时任务状态
    """
    # 加载配置
    config_path = Path(__file__).parent.parent.parent.parent / 'code' / 'backend' / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 创建调度器
    scheduler = DataScheduler(config)

    # 启动调度器
    scheduler.start()

    # 查看任务状态
    print("\n定时任务状态：")
    print("=" * 80)
    status = scheduler.get_jobs_status()
    for job_id, job_info in status.items():
        print(f"任务ID: {job_id}")
        print(f"  名称: {job_info['name']}")
        print(f"  下次执行: {job_info['next_run_time']}")
        print(f"  触发器: {job_info['trigger']}")
        print("-" * 80)

    # 保持运行（测试用）
    print("\n调度器正在运行，按Ctrl+C停止...")
    try:
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.stop()
        print("\n调度器已停止")


if __name__ == '__main__':
    main()