#!/bin/bash
# AData 系统服务安装脚本

echo "========== 创建后端服务 =========="
sudo tee /etc/systemd/system/adata-backend.service > /dev/null <<'EOF'
[Unit]
Description=AData Backend
After=network.target

[Service]
Type=simple
User=my
WorkingDirectory=/home/my/claude-project/AData
Environment="PATH=/home/my/claude-project/AData/venv/bin:/usr/bin"
ExecStart=/home/my/claude-project/AData/venv/bin/python3 /home/my/claude-project/AData/code/backend/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "========== 创建前端服务 =========="
sudo tee /etc/systemd/system/adata-frontend.service > /dev/null <<'EOF'
[Unit]
Description=AData Frontend
After=network.target

[Service]
Type=simple
User=my
WorkingDirectory=/home/my/claude-project/AData
Environment="PATH=/home/my/claude-project/AData/venv/bin:/usr/bin"
ExecStart=/home/my/claude-project/AData/venv/bin/python3 /home/my/claude-project/AData/code/frontend/run_dashboard.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "========== 重新加载systemd =========="
sudo systemctl daemon-reload

echo "========== 配置开机自启 =========="
sudo systemctl enable adata-backend
sudo systemctl enable adata-frontend

echo "========== 启动服务 =========="
sudo systemctl start adata-backend
sudo systemctl start adata-frontend

echo "========== 查看服务状态 =========="
sudo systemctl status adata-backend --no-pager
echo ""
sudo systemctl status adata-frontend --no-pager

echo ""
echo "✓ 安装完成！"
echo ""
echo "常用命令："
echo "  查看状态: sudo systemctl status adata-backend"
echo "  停止服务: sudo systemctl stop adata-backend"
echo "  启动服务: sudo systemctl start adata-backend"
echo "  重启服务: sudo systemctl restart adata-backend"
echo "  查看日志: sudo journalctl -u adata-backend -f"
