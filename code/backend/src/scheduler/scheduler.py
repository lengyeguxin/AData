"""
定时任务调度器

功能：
- 18:00定时拉取日线数据
- 30分钟定时快照生成
- 周/月线数据定时拉取
- 异常处理和重试机制
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
        self.daily_update_time = scheduler_config.get('daily_update_time', '18:00')
        self.snapshot_interval = config.get('snapshot', {}).get('interval', 30)

        self.logger.info(f"调度器初始化完成")
        self.logger.info(f"日线更新时间: {self.daily_update_time}")
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

        # 3. 启动调度器
        self.scheduler.start()
        self.logger.info("✓ 定时任务调度器已启动")

    def stop(self):
        """停止调度器"""
        self.logger.info("停止定时任务调度器...")
        self.scheduler.shutdown()
        self.logger.info("✓ 定时任务调度器已停止")

    def add_daily_fetch_job(self):
        """
        添加日线数据定时拉取任务

        时间：每天18:00（可配置）
        任务：拉取所有需要更新的数据
        """
        # 解析时间
        hour, minute = self.daily_update_time.split(':')
        hour = int(hour)
        minute = int(minute)

        # 创建cron触发器
        trigger = CronTrigger(hour=hour, minute=minute)

        # 添加任务
        self.scheduler.add_job(
            self.fetch_daily_data,
            trigger,
            id='daily_fetch',
            name='日线数据拉取',
            max_instances=1,  # 只允许一个实例运行
            misfire_grace_time=3600  # 允许1小时内的延迟执行
        )

        self.logger.info(f"✓ 已添加日线数据拉取任务: 每天{self.daily_update_time}")

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

    def fetch_daily_data(self):
        """
        拉取日线数据任务

        任务内容：
        - 拉取所有需要更新的表
        - 异常处理和日志记录
        """
        self.logger.info("=" * 80)
        self.logger.info("开始定时拉取日线数据...")
        self.logger.info(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            # 调用DataFetcher拉取数据
            self.fetcher.start()

            self.logger.info("✓ 日线数据拉取完成")

        except Exception as e:
            self.logger.error(f"✗ 日线数据拉取失败: {e}")
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