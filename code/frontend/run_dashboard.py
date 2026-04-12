#!/usr/bin/env python3
"""
A股数据库监控面板启动脚本

启动Streamlit应用，访问地址: http://localhost:8501
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import streamlit.web.cli as stcli

    # 设置Streamlit配置
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = 'localhost'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

    # Streamlit启动参数
    sys.argv = [
        "streamlit",
        "run",
        str(project_root / "dashboard" / "app.py"),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false",
        "--theme.base=light"
    ]

    print("=" * 70)
    print("A股数据库监控面板")
    print("=" * 70)
    print(f"访问地址: http://localhost:8501")
    print(f"数据库: {project_root / 'data' / 'adata.db'}")
    print("=" * 70)
    print()

    # 启动Streamlit
    sys.exit(stcli.main())