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
from typing import Dict, List, Optional
from src.core.logger import get_logger


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
        """
        self.token = config.get('token', '')
        self.api_url = config.get('api_url', 'http://api.tushare.pro')
        self.rate_limit = config.get('rate_limit', 500)  # 每分钟500次

        self.logger = get_logger(__name__)

        # 速率控制
        self.last_request_time = 0
        self.request_interval = 60.0 / self.rate_limit  # 每次请求间隔（秒）

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

        # 速率控制（避免超过每分钟限制）
        self._rate_limit_control()

        # 构建请求参数
        params = {
            'api_name': api_name,
            'token': self.token,
            'params': kwargs,
            'fields': ''  # 返回所有字段
        }

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
                self.logger.error(f"API调用失败: {api_name} - {error_msg}")
                raise Exception(f"Tushare API错误: {error_msg}")

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

        except requests.Timeout:
            self.logger.error(f"API请求超时: {api_name}")
            raise Exception("API请求超时")

        except requests.RequestException as e:
            self.logger.error(f"API请求失败: {api_name} - {e}")
            raise Exception(f"API请求失败: {e}")

    def _rate_limit_control(self):
        """
        速率控制（避免超过每分钟限制）

        策略：
        - 记录上次请求时间
        - 每次请求间隔 ≥ 60秒/速率限制
        - 例如：500次/分钟 → 每次0.12秒间隔
        """
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time

        if elapsed_time < self.request_interval:
            sleep_time = self.request_interval - elapsed_time
            time.sleep(sleep_time)

        self.last_request_time = time.time()

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