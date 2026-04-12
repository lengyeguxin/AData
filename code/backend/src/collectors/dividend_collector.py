"""
${collector} Collector - 自动生成模板
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))
from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format

class ${collector}Collector(BaseCollector):
    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(db_path=db_path, api=api, table_name='${collector}', api_name='${collector}', date_field='trade_date', vip_interface=False)
    
    def collect_by_date(self, trade_date: str) -> List[Dict]:
        self.logger.info(f"拉取${collector}: trade_date={trade_date}")
        return self.collect(trade_date=trade_date)
    
    def _extract_values(self, item: Dict) -> tuple:
        return (item.get('ts_code'), convert_date_format(item.get('trade_date')), item.get('value'))
    
    def _build_insert_query(self) -> str:
        return f"INSERT INTO {collector} (ts_code, trade_date, value, updated_at) VALUES (?, ?, ?, NOW()) ON CONFLICT (ts_code, trade_date) DO UPDATE SET value = excluded.value, updated_at = NOW()"
    
    def run_by_date(self, trade_date: str) -> int:
        data = self.collect_by_date(trade_date)
        return self.save(data)
