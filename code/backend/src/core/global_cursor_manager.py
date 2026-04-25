"""
全局游标管理器

负责管理27张数据表的游标状态，包括：
- 游标策略判断（5种策略：none/daily_trade/daily_natural/yearly/special_ths_member）
- 数据拉取进度判断（should_fetch）
- 18点时间判断逻辑
- 游标更新时机判断（财务表允许无数据更新）
- 线程安全：Per-Table Lock保证游标更新无竞态条件
"""

import yaml
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 使用Database类统一管理连接
from src.core.database import Database


class GlobalCursorManager:
    """全局游标管理器（每表一个游标，线程安全）"""

    # 游标策略常量
    CURSOR_STRATEGY_NONE = 'none'                  # 无游标，全量拉取
    CURSOR_STRATEGY_DAILY_TRADE = 'daily_trade'    # 按天记录（交易日）
    CURSOR_STRATEGY_DAILY_NATURAL = 'daily_natural' # 按天记录（自然日）
    CURSOR_STRATEGY_YEARLY = 'yearly'              # 按年记录
    CURSOR_STRATEGY_SPECIAL_THS_MEMBER = 'special_ths_member' # 特殊游标

    # 状态常量
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_SUCCESS = 'success'
    STATUS_FAILED = 'failed'

    def __init__(self, db_path: str, config_path: str = 'code/backend/config'):
        """
        初始化全局游标管理器

        Args:
            db_path: 数据库路径
            config_path: 配置文件路径
        """
        self.db_path = db_path
        self.config_path = Path(config_path)

        # 初始化logger
        from src.core.logger import get_logger
        self.logger = get_logger(__name__)

        # 线程安全：Per-Table Lock（每个表独立的锁）
        self.table_locks = {}  # {table_name: Lock}
        self.locks_lock = threading.Lock()  # 保护字典

        # 加载配置
        self.config = self._load_config()

        # 加载table_config（__init__中加载，确保总是可用）
        self.table_config = self._load_table_config()

    def _get_table_lock(self, table_name: str) -> threading.Lock:
        """
        获取或创建表锁（线程安全）

        Args:
            table_name: 表名

        Returns:
            表锁对象
        """
        with self.locks_lock:
            if table_name not in self.table_locks:
                self.table_locks[table_name] = threading.Lock()
            return self.table_locks[table_name]

    def initialize(self):
        """
        初始化游标表（创建global_cursor表和索引）

        Returns:
            bool: 是否初始化成功
        """
        try:
            # 读取schema SQL文件
            schema_file = self.config_path.parent.parent.parent / 'database' / 'schemas' / 'global_cursor_schema.sql'
            if not schema_file.exists():
                self.logger.warning(f"global_cursor_schema.sql不存在，使用默认SQL创建")
                # 使用默认SQL创建表
                create_sql = """
                    CREATE TABLE IF NOT EXISTS global_cursor (
                        table_name VARCHAR(50) PRIMARY KEY,
                        cursor_strategy VARCHAR(20) NOT NULL,
                        cursor_value VARCHAR(20),
                        dependencies TEXT,
                        fetch_after_time VARCHAR(10),
                        last_fetch_time TIMESTAMP,
                        last_record_count INTEGER DEFAULT 0,
                        status VARCHAR(10) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    );
                    CREATE INDEX IF NOT EXISTS idx_cursor_strategy ON global_cursor(cursor_strategy);
                """
                # 使用Database类统一管理连接
                db = Database(self.db_path)
                db.execute(create_sql)
                db.close()
            else:
                # 从schema文件读取并执行
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                # 使用Database类统一管理连接
                db = Database(self.db_path)
                db.execute(schema_sql)
                db.close()

            self.logger.info(f"游标表初始化成功: {self.db_path}")
            return True

        except Exception as e:
            self.logger.error(f"游标表初始化失败: {e}")
            return False

    def _load_config(self) -> Dict:
        """加载主配置文件"""
        config_file = self.config_path / 'config.yaml'
        if not config_file.exists():
            # 默认配置
            return {
                'fetch': {
                    'start_date': '20210101',
                    'enabled': True
                },
                'scheduler': {
                    'daily_update_time': '18:00'
                }
            }

        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_table_config(self) -> Dict:
        """加载表配置文件"""
        table_config_file = self.config_path / 'table_config.yaml'
        if not table_config_file.exists():
            return {}

        with open(table_config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_cursor(self, table_name: str) -> Optional[Dict]:
        """
        获取表的游标信息

        Args:
            table_name: 表名

        Returns:
            游标信息字典，包含cursor_value, cursor_strategy, status等
        """
        query = """
            SELECT table_name, cursor_strategy, cursor_value, dependencies,
                   fetch_after_time, last_fetch_time, last_record_count, status,
                   created_at, updated_at
            FROM global_cursor
            WHERE table_name = ?
        """

        # 使用Database类统一管理连接
        db = Database(self.db_path)
        result = db.execute(query, (table_name,))
        db.close()

        if not result:
            return None

        row = result[0]
        return {
            'table_name': row[0],
            'cursor_strategy': row[1],
            'cursor_value': row[2],
            'dependencies': row[3].split(',') if row[3] else [],
            'fetch_after_time': row[4],
            'last_fetch_time': str(row[5]) if row[5] else None,
            'last_record_count': row[6],
            'status': row[7],
            'created_at': str(row[8]) if row[8] else None,
            'updated_at': str(row[9]) if row[9] else None
        }

    def should_fetch(self, table_name: str) -> bool:
        """
        判断是否需要拉取（单线程：只通过游标值判断）

        Args:
            table_name: 表名

        Returns:
            是否需要拉取
        """
        cursor = self.get_cursor(table_name)

        if not cursor:
            return True  # 首次拉取

        # 只通过 cursor_value 判断是否需要拉取
        # None：从未拉取过，需要拉取
        # 有值：已拉取过，通过日期/时间判断是否需要更新
        cursor_value = cursor['cursor_value']

        if cursor_value is None or cursor_value == '':
            return True  # 从未拉取过，需要拉取

        # 已拉取过，检查游标是否最新
        # 游标最新 → 不拉取
        # 游标不是最新 → 立即拉取（忽略时间限制）
        if self._is_cursor_up_to_date(table_name, cursor):
            return False

        # 游标不是最新（有历史gap），直接允许拉取
        return True

    def check_dependencies(self, table_name: str) -> bool:
        """
        检查前置表是否完成

        Args:
            table_name: 表名

        Returns:
            前置表是否都已完成
        """
        cursor = self.get_cursor(table_name)
        if not cursor or not cursor['dependencies']:
            return True

        for dep_table in cursor['dependencies']:
            dep_cursor = self.get_cursor(dep_table)
            if not dep_cursor or dep_cursor['status'] != self.STATUS_SUCCESS:
                return False

        return True

    def check_fetch_time(self, table_name: str) -> bool:
        """
        检查是否在允许拉取时间后（如18:00后）

        Args:
            table_name: 表名

        Returns:
            是否已到允许拉取时间
        """
        cursor = self.get_cursor(table_name)
        if not cursor or not cursor['fetch_after_time']:
            return True

        # 解析截至时间（如'18:00'）
        try:
            hour, minute = cursor['fetch_after_time'].split(':')
            fetch_time = datetime.now().replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        except:
            return True

        return datetime.now() >= fetch_time

    def get_next_fetch_date(self, table_name: str) -> str:
        """
        获取下次拉取的日期（游标值+1）

        Args:
            table_name: 表名

        Returns:
            下次拉取的日期（YYYYMMDD或YYYY或YYYYMM）
        """
        cursor = self.get_cursor(table_name)

        if not cursor or not cursor['cursor_value']:
            # 从配置的start_date开始
            return self._get_start_date_from_config(table_name)

        cursor_value = cursor['cursor_value']
        cursor_strategy = cursor['cursor_strategy']

        # 根据游标策略计算下次日期
        if cursor_strategy == self.CURSOR_STRATEGY_DAILY_TRADE or \
           cursor_strategy == self.CURSOR_STRATEGY_DAILY_NATURAL:
            # YYYYMMDD + 1天
            try:
                date = datetime.strptime(cursor_value, '%Y%m%d')
                next_date = date + timedelta(days=1)
                return next_date.strftime('%Y%m%d')
            except:
                return self._get_start_date_from_config(table_name)

        elif cursor_strategy == self.CURSOR_STRATEGY_YEARLY:
            # YYYY + 1年
            try:
                year = int(cursor_value)
                return str(year + 1)
            except:
                return self._get_start_date_from_config(table_name)

        elif cursor_strategy == self.CURSOR_STRATEGY_NONE:
            # 无游标，返回当前日期
            return datetime.now().strftime('%Y%m%d')

        elif cursor_strategy == self.CURSOR_STRATEGY_SPECIAL_THS_MEMBER:
            # 特殊游标（ths_concept_member），返回当前指数代码
            return cursor_value

        return cursor_value

    def get_end_date_with_time_check(self, table_name: str) -> str:
        """
        获取结束日期（带18点时间判断）

        Args:
            table_name: 表名

        Returns:
            YYYYMMDD格式的结束日期
            - 当前时间≥截止时间：返回今天日期
            - 当前时间<截止时间：返回昨日日期
        """
        cursor = self.get_cursor(table_name)

        # 获取截止时间（默认18:00）
        fetch_after_time = cursor.get('fetch_after_time', '18:00') if cursor else '18:00'

        try:
            hour, minute = fetch_after_time.split(':')
            fetch_after_hour = int(hour)
        except:
            fetch_after_hour = 18

        now = datetime.now()

        if now.hour >= fetch_after_hour:
            # 当前时间≥截止时间，使用今天日期
            return now.strftime('%Y%m%d')
        else:
            # 当前时间<截止时间，使用昨日日期
            yesterday = now - timedelta(days=1)
            return yesterday.strftime('%Y%m%d')

    def update_cursor(self, table_name: str, cursor_value: str, record_count: int):
        """
        更新游标（线程安全，只有所有数据入库成功才更新）

        Args:
            table_name: 表名
            cursor_value: 新的游标值（已完成的最后日期）
            record_count: 拉取的记录数
        """
        # 线程安全：获取表锁
        table_lock = self._get_table_lock(table_name)

        with table_lock:
            self.logger.info(f"Updating cursor for {table_name}: {cursor_value} ({record_count} records)")

            # DuckDB UPDATE PRIMARY KEY有BUG，使用DELETE + INSERT方式
            query_get = """
                SELECT cursor_strategy, dependencies, fetch_after_time, created_at
                FROM global_cursor
                WHERE table_name = ?
            """

            query_delete = "DELETE FROM global_cursor WHERE table_name = ?"

            query_insert = """
                INSERT INTO global_cursor (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, last_fetch_time, last_record_count,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, NOW(), ?, ?, ?, NOW())
            """

            # 使用Database类统一管理连接，使用事务包裹DELETE+INSERT
            db = Database(self.db_path)

            try:
                # 开启事务（原子性，避免索引损坏）
                db.execute("BEGIN TRANSACTION")

                # 1. 获取原始记录信息
                result = db.execute(query_get, (table_name,))
                if not result:
                    self.logger.error(f"No cursor found for {table_name}")
                    db.execute("ROLLBACK")
                    db.close()
                    return

                cursor_strategy = result[0][0]
                dependencies = result[0][1]
                fetch_after_time = result[0][2]
                created_at = result[0][3]

                # 2. 删除旧记录
                db.execute(query_delete, (table_name,))

                # 3. 插入新记录（更新cursor_value和status）
                db.execute(query_insert, (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, record_count, self.STATUS_SUCCESS, created_at
                ))

                # 提交事务
                db.execute("COMMIT")
                self.logger.info(f"Cursor updated successfully for {table_name}")

            except Exception as e:
                # 异常时回滚
                db.execute("ROLLBACK")
                self.logger.error(f"Failed to update cursor for {table_name}: {e}")
                raise

            finally:
                db.close()

    def mark_running(self, table_name: str):
        """标记为正在拉取（线程安全，DuckDB兼容：DELETE + INSERT）"""
        # 线程安全：获取表锁
        table_lock = self._get_table_lock(table_name)

        with table_lock:
            # DuckDB UPDATE PRIMARY KEY有BUG，使用DELETE + INSERT方式
            query_get = """
                SELECT cursor_strategy, cursor_value, dependencies, fetch_after_time,
                       last_fetch_time, last_record_count, created_at
                FROM global_cursor
                WHERE table_name = ?
            """

            query_delete = "DELETE FROM global_cursor WHERE table_name = ?"

            query_insert = """
                INSERT INTO global_cursor (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, last_fetch_time, last_record_count,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            """

            db = Database(self.db_path)

            try:
                # 开启事务（原子性，避免索引损坏）
                db.execute("BEGIN TRANSACTION")

                # 1. 获取原始记录信息
                result = db.execute(query_get, (table_name,))
                if not result:
                    self.logger.error(f"No cursor found for {table_name}")
                    db.execute("ROLLBACK")
                    db.close()
                    return

                row = result[0]
                cursor_strategy = row[0]
                cursor_value = row[1]
                dependencies = row[2]
                fetch_after_time = row[3]
                last_fetch_time = row[4]
                last_record_count = row[5]
                created_at = row[6]

                # 2. 删除旧记录
                db.execute(query_delete, (table_name,))

                # 3. 插入新记录（更新status为running）
                db.execute(query_insert, (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, last_fetch_time, last_record_count,
                    self.STATUS_RUNNING, created_at
                ))

                # 提交事务
                db.execute("COMMIT")

            except Exception as e:
                # 异常时回滚
                db.execute("ROLLBACK")
                self.logger.error(f"Failed to mark {table_name} as running: {e}")
                raise

            finally:
                db.close()

    def mark_failed(self, table_name: str, error_message: str = ""):
        """标记为失败（线程安全，DuckDB兼容：DELETE + INSERT）"""
        # 线程安全：获取表锁
        table_lock = self._get_table_lock(table_name)

        with table_lock:
            # DuckDB UPDATE PRIMARY KEY有BUG，使用DELETE + INSERT方式
            query_get = """
                SELECT cursor_strategy, cursor_value, dependencies, fetch_after_time,
                       last_fetch_time, last_record_count, created_at
                FROM global_cursor
                WHERE table_name = ?
            """

            query_delete = "DELETE FROM global_cursor WHERE table_name = ?"

            query_insert = """
                INSERT INTO global_cursor (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, last_fetch_time, last_record_count,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            """

            db = Database(self.db_path)

            try:
                # 开启事务（原子性，避免索引损坏）
                db.execute("BEGIN TRANSACTION")

                # 1. 获取原始记录信息
                result = db.execute(query_get, (table_name,))
                if not result:
                    self.logger.error(f"No cursor found for {table_name}")
                    db.execute("ROLLBACK")
                    db.close()
                    return

                row = result[0]
                cursor_strategy = row[0]
                cursor_value = row[1]
                dependencies = row[2]
                fetch_after_time = row[3]
                last_fetch_time = row[4]
                last_record_count = row[5]
                created_at = row[6]

                # 2. 删除旧记录
                db.execute(query_delete, (table_name,))

                # 3. 插入新记录（更新status为failed）
                db.execute(query_insert, (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, last_fetch_time, last_record_count,
                    self.STATUS_FAILED, created_at
                ))

                # 提交事务
                db.execute("COMMIT")

            except Exception as e:
                # 异常时回滚
                db.execute("ROLLBACK")
                self.logger.error(f"Failed to mark {table_name} as failed: {e}")
                raise

            finally:
                db.close()

    def should_update_cursor(self, table_name: str, has_data: bool) -> bool:
        """
        判断是否应该更新游标（根据策略）

        Args:
            table_name: 表名
            has_data: 是否有数据（拉取的记录数>0）

        Returns:
            是否应该更新游标
            - 财务表（按自然日）：允许无数据更新（ann_date可能无数据）
            - 其他表：必须有数据才更新（无数据则报错）
        """
        cursor = self.get_cursor(table_name)
        if not cursor:
            return False

        cursor_strategy = cursor['cursor_strategy']

        # 财务表（按自然日），允许无数据更新
        if cursor_strategy == self.CURSOR_STRATEGY_DAILY_NATURAL:
            return True

        # 其他表，必须有数据才更新
        return has_data

    def get_all_cursors(self) -> List[Dict]:
        """
        获取所有游标状态（用于Dashboard展示）

        Returns:
            游标状态列表
        """
        query = """
            SELECT table_name, cursor_strategy, cursor_value, status,
                   last_fetch_time, last_record_count, dependencies, fetch_after_time
            FROM global_cursor
            ORDER BY table_name
        """

        # 使用Database类统一管理连接
        db = Database(self.db_path)
        results = db.execute(query)
        db.close()

        cursors = []
        for row in results:
            cursors.append({
                'table_name': row[0],
                'cursor_strategy': row[1],
                'cursor_value': row[2],
                'status': row[3],
                'last_fetch_time': str(row[4]) if row[4] else None,
                'last_record_count': row[5],
                'dependencies': row[6].split(',') if row[6] else [],
                'fetch_after_time': row[7]
            })

        return cursors

    def get_cursor_strategy(self, table_name: str) -> str:
        """
        获取表的游标策略

        Args:
            table_name: 表名

        Returns:
            游标策略类型
        """
        cursor = self.get_cursor(table_name)
        if not cursor:
            return self.CURSOR_STRATEGY_NONE

        return cursor['cursor_strategy']

    def _is_cursor_up_to_date(self, table_name: str, cursor: Dict) -> bool:
        """
        判断游标是否已是最新（不需要再拉取）

        Args:
            table_name: 表名
            cursor: 游标信息

        Returns:
            游标是否已是最新
        """
        # 获取当前最新日期
        now = datetime.now()

        cursor_strategy = cursor['cursor_strategy']
        cursor_value = cursor['cursor_value']

        if not cursor_value:
            return False

        if cursor_strategy == self.CURSOR_STRATEGY_DAILY_TRADE:
            # 日线数据：检查是否是今天或昨天（交易日）
            # 使用18点判断
            end_date = self.get_end_date_with_time_check(table_name)
            return cursor_value >= end_date

        elif cursor_strategy == self.CURSOR_STRATEGY_DAILY_NATURAL:
            # 财务数据（自然日）：检查是否是今天
            today = now.strftime('%Y%m%d')
            return cursor_value == today

        elif cursor_strategy == self.CURSOR_STRATEGY_YEARLY:
            # 年度数据：检查是否是今年
            current_year = str(now.year)
            return cursor_value == current_year

        elif cursor_strategy == self.CURSOR_STRATEGY_NONE:
            # 一次性数据（基础信息表）：月更新策略
            # 检查last_fetch_time是否在本月
            last_fetch_time = cursor.get('last_fetch_time')
            if last_fetch_time:
                try:
                    # 解析last_fetch_time
                    if isinstance(last_fetch_time, str):
                        last_date = datetime.strptime(last_fetch_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    else:
                        last_date = last_fetch_time

                    # 比较月份：同月则不更新，不同月则更新
                    current_month = now.strftime('%Y%m')
                    last_month = last_date.strftime('%Y%m')
                    return current_month == last_month
                except:
                    return False
            return False  # 没有last_fetch_time，需要拉取

        elif cursor_strategy == self.CURSOR_STRATEGY_SPECIAL_THS_MEMBER:
            # 特殊游标（ths_concept_member）：月更新策略
            # 检查last_fetch_time是否在本月
            last_fetch_time = cursor.get('last_fetch_time')
            if last_fetch_time:
                try:
                    # 解析last_fetch_time
                    if isinstance(last_fetch_time, str):
                        last_date = datetime.strptime(last_fetch_time.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    else:
                        last_date = last_fetch_time

                    # 比较月份：同月则不更新，不同月则更新
                    current_month = now.strftime('%Y%m')
                    last_month = last_date.strftime('%Y%m')
                    return current_month == last_month
                except:
                    return False
            return False  # 没有last_fetch_time，需要拉取

        return False

    def _get_start_date_from_config(self, table_name: str) -> str:
        """
        从配置获取起始日期

        Args:
            table_name: 表名

        Returns:
            起始日期（YYYYMMDD）
        """
        # 从table_config.yaml获取
        if table_name in self.table_config.get('tables', {}):
            start_date = self.table_config['tables'][table_name].get('start_date')
            if start_date:
                return start_date

        # 从config.yaml获取全局start_date
        start_date = self.config.get('fetch', {}).get('start_date', '20210101')
        return start_date

    def reset_cursor(self, table_name: str):
        """
        重置单张表的游标（清除进度）

        Args:
            table_name: 表名
        """
        query = """
            UPDATE global_cursor
            SET cursor_value = NULL,
                status = ?,
                last_record_count = 0,
                updated_at = NOW()
            WHERE table_name = ?
        """

        # 使用Database类统一管理连接
        db = Database(self.db_path)
        db.execute(query, (self.STATUS_PENDING, table_name))
        db.close()

    def reset_all_cursors(self):
        """重置所有表的游标"""
        query = """
            UPDATE global_cursor
            SET cursor_value = NULL,
                status = ?,
                last_record_count = 0,
                updated_at = NOW()
        """

        # 使用Database类统一管理连接
        db = Database(self.db_path)
        db.execute(query, (self.STATUS_PENDING,))
        db.close()