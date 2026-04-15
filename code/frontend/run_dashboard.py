#!/usr/bin/env python3
"""
A股数据库监控面板启动脚本

启动Streamlit应用，访问地址: http://localhost:8501

使用Dashboard独立的配置系统（config/dashboard_config.yaml）
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import streamlit.web.cli as stcli

    # 导入Dashboard配置管理器
    try:
        from dashboard.config import get_dashboard_config_manager
        config = get_dashboard_config_manager()

        # 从配置文件读取配置
        server_config = config.get_server_config()
        host = server_config.get('host', 'localhost')
        port = server_config.get('port', 8501)
        debug = server_config.get('debug', False)

        # 获取数据库路径
        db_path = config.get_database_path()
    except Exception as e:
        print(f"警告: 无法加载配置文件，使用默认配置: {e}")
        # 使用默认配置
        host = 'localhost'
        port = 8501
        db_path = project_root / 'data' / 'adata.db'
        debug = False

    # 设置Streamlit配置
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    os.environ['STREAMLIT_SERVER_ADDRESS'] = host
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

    # Streamlit启动参数
    sys.argv = [
        "streamlit",
        "run",
        str(project_root / "dashboard" / "app.py"),
        f"--server.port={port}",
        f"--server.address={host}",
        "--browser.gatherUsageStats=false",
        "--theme.base=light"
    ]

    if debug:
        sys.argv.append("--logger.level=debug")

    print("=" * 70)
    print("A股数据库监控面板")
    print("=" * 70)
    print(f"访问地址: http://{host}:{port}")
    print(f"数据库: {db_path}")
    print(f"调试模式: {debug}")
    print("=" * 70)
    print()

    # 启动Streamlit
    sys.exit(stcli.main())
