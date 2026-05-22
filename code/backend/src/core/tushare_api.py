"""
TushareAPI封装

封装Tushare Pro API，严格按照CSV文档的接口名称和参数规范：
- VIP接口：fina_indicator_vip、income_vip、balancesheet_vip、cashflow_vip、forecast_vip、express_vip
- 标准接口：daily、daily_basic、trade_cal、stock_basic、index_basic、dividend等
- 速率控制：500次/分钟（1万积分）
"""

import time
import requests
import json
import threading
import random
from collections import deque
from typing import Dict, List, Optional
from src.core.logger import get_logger


class ThreadSafeRateLimiter:
    """
    线程安全限流器（Sliding Window算法）
    - 保证全局500 req/min
    - 线程锁保护时间戳队列
    - 自动等待当超限时
    """

    def __init__(self, rate_limit: int = 500, window_seconds: int = 60):
        """
        初始化限流器

        Args:
            rate_limit: 时间窗口内最大请求数（默认500）
            window_seconds: 时间窗口大小（默认60秒）
        """
        self.rate_limit = rate_limit
        self.window_seconds = window_seconds
        self.request_timestamps = deque(maxlen=rate_limit)
        self.lock = threading.Lock()  # 保护队列
        self.logger = get_logger(__name__)

    def acquire(self):
        """
        获取请求许可（阻塞直到限流允许）
        - 移除过期时间戳
        - 检查是否可请求
        - 计算等待时间并阻塞
        """
        with self.lock:
            # 移除过期时间戳（超过时间窗口）
            now = time.time()
            while self.request_timestamps and self.request_timestamps[0] < now - self.window_seconds:
                self.request_timestamps.popleft()

            # 检查是否可请求
            if len(self.request_timestamps) < self.rate_limit:
                self.request_timestamps.append(now)
                return True

            # 计算等待时间（等待最早的时间戳过期）
            wait_time = self.request_timestamps[0] + self.window_seconds - now
            if wait_time > 0:
                self.logger.info(f"限流等待: {wait_time:.2f}秒（已达到{self.rate_limit}次/分钟限制）")

        # 在锁外等待（避免阻塞其他线程）
        time.sleep(wait_time)
        return self.acquire()  # 重试


class TushareAPI:
    """TushareAPI封装类"""

    # VIP接口列表（财务表）
    VIP_INTERFACES = [
        'fina_indicator_vip',
        'income_vip',
        'balancesheet_vip',
        'cashflow_vip',
        'forecast_vip',      # 业绩预告VIP接口
        'express_vip'        # 业绩快报VIP接口
    ]

    def __init__(self, config: Dict):
        """
        初始化TushareAPI

        Args:
            config: Tushare配置字典
                - token: API Token
                - api_url: API地址
                - rate_limit: 速率限制（次/分钟）
                - random_sleep_min: 随机休眠最小值（秒）
                - random_sleep_max: 随机休眠最大值（秒）
        """
        self.token = config.get('token', '')
        self.api_url = config.get('api_url', 'http://8.136.22.187:8010/')  # 新代理地址
        self.rate_limit = config.get('rate_limit', 500)  # 每分钟500次
        self.random_sleep_min = config.get('random_sleep_min', 1)  # 默认最小1秒
        self.random_sleep_max = config.get('random_sleep_max', 3)  # 默认最大3秒

        self.logger = get_logger(__name__)

        # 线程安全速率控制
        self.rate_limiter = ThreadSafeRateLimiter(
            rate_limit=self.rate_limit,
            window_seconds=60
        )

    def query(self, api_name: str, **kwargs) -> List[Dict]:
        """
        查询Tushare API

        Args:
            api_name: API名称（严格按照CSV文档）
            **kwargs: API参数

        Returns:
            数据列表（字典格式）

        示例：
            # 标准接口
            api.query('daily', trade_date='20260409', adj='null')
            api.query('stock_basic')

            # VIP接口（财务表）
            api.query('fina_indicator_vip', ann_date='20260409')
            api.query('income_vip', ann_date='20260409', report_type='1')
        """
        self.logger.info(f"调用API: {api_name}, 参数: {kwargs}")

        # 线程安全速率控制（自动阻塞等待）
        self.rate_limiter.acquire()

        # 随机休眠（避免过于频繁请求）
        # 如果max设置为0，则禁用休眠
        if self.random_sleep_max > 0:
            sleep_time = random.uniform(self.random_sleep_min, self.random_sleep_max)
            self.logger.info(f"随机休眠: {sleep_time:.2f}秒")
            time.sleep(sleep_time)

        # 构建请求参数
        params = {
            'api_name': api_name,
            'token': self.token,
            'params': kwargs,
            'fields': ''  # 返回所有字段
        }

        # 速率限制重试机制
        max_rate_limit_retries = 3
        rate_limit_retry_count = 0

        while rate_limit_retry_count < max_rate_limit_retries:
            # 发送POST请求
            try:
                response = requests.post(
                    self.api_url,
                    data=json.dumps(params),
                    headers={'Content-Type': 'application/json'},
                    timeout=60  # VIP接口需要更长超时时间
                )

                response_data = response.json()

                # 检查返回状态
                if response_data.get('code') != 0:
                    error_msg = response_data.get('msg', '未知错误')

                    # 特殊处理速率限制错误
                    if '您请求速度过快' in error_msg or '请求速度过快' in error_msg:
                        rate_limit_retry_count += 1
                        if rate_limit_retry_count < max_rate_limit_retries:
                            self.logger.warning(
                                f"API速率限制触发: {api_name} - {error_msg} "
                                f"(第{rate_limit_retry_count}次，休眠60秒后重试)"
                            )
                            time.sleep(60)  # 休眠60秒
                            continue  # 重试请求
                        else:
                            self.logger.error(
                                f"API速率限制重试失败: {api_name} - {error_msg} "
                                f"(已重试{max_rate_limit_retries}次)"
                            )
                            raise Exception(f"Tushare API错误: {error_msg}")

                    # 其他错误直接抛出
                    self.logger.error(f"API调用失败: {api_name} - {error_msg}")
                    raise Exception(f"Tushare API错误: {error_msg}")

                # 成功获取数据，退出重试循环
                break

            except requests.Timeout:
                self.logger.error(f"API请求超时: {api_name}")
                raise Exception("API请求超时")

            except requests.RequestException as e:
                self.logger.error(f"API请求失败: {api_name} - {e}")
                raise Exception(f"API请求失败: {e}")

        # 获取数据（新格式：data包含fields和items）
        data_dict = response_data.get('data', {})

        if not data_dict:
            self.logger.warning(f"API返回空数据: {api_name}")
            return []

        # 解析数据格式
        # API返回格式：
        # {
        #   "data": {
        #     "fields": ["ts_code", "name", ...],
        #     "items": [["000001.SZ", "平安银行", ...], ...]
        #   }
        # }

        fields = data_dict.get('fields', [])
        items = data_dict.get('items', [])

        if not fields or not items:
            # 兼容旧格式（直接返回列表）
            self.logger.warning(f"API返回格式异常: {api_name}")
            return []

        # 将二维数组转换为字典列表
        result = []
        for item in items:
            row_dict = {}
            for i, field in enumerate(fields):
                row_dict[field] = item[i] if i < len(item) else None
            result.append(row_dict)

        self.logger.info(f"API返回数据: {len(result)}条记录")

        return result

        except requests.RequestException as e:
            self.logger.error(f"API请求失败: {api_name} - {e}")
            raise Exception(f"API请求失败: {e}")

    def is_vip_interface(self, api_name: str) -> bool:
        """
        判断是否VIP接口

        Args:
            api_name: API名称

        Returns:
            是否VIP接口
        """
        return api_name in self.VIP_INTERFACES

    def get_api_doc_url(self, api_name: str) -> str:
        """
        获取API文档地址（用于日志记录）

        Args:
            api_name: API名称

        Returns:
            文档URL（根据CSV文档映射）
        """
        # API名称到文档ID映射（从CSV文档）
        api_doc_mapping = {
            'trade_cal': '26',
            'stock_basic': '25',
            'daily': '27',
            'daily_basic': '32',
            'stk_week_month_adj': '365',
            'index_basic': '94',
            'index_daily': '95',
            'etf_basic': '385',
            'etf_index': '386',
            'fund_daily': '127',
            'fund_adj': '199',
            'ths_index': '259',
            'ths_member': '261',
            'ths_daily': '260',
            'fina_indicator_vip': '79',
            'income_vip': '33',
            'balancesheet_vip': '36',
            'cashflow_vip': '44',
            'forecast_vip': '45',
            'express_vip': '46',
            'dividend': '103',
            'moneyflow_ths': '348',
            'moneyflow_cnt_ths': '371',
            'moneyflow_ind_ths': '343',
            'hots_user': '272',
            'hots_trader_detail': '273'
        }

        doc_id = api_doc_mapping.get(api_name, '')

        if doc_id:
            return f"https://tushare.pro/document/2?doc_id={doc_id}"

        return "https://tushare.pro/document/2"