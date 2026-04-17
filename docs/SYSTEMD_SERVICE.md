# AData 系统服务配置

## 快速安装

```bash
cd /home/my/claude-project/AData
bash docs/service-install.sh
```

## 服务文件

### 后端服务 (/etc/systemd/system/adata-backend.service)

```ini
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
```

### 前端服务 (/etc/systemd/system/adata-frontend.service)

```ini
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
```

## 手动安装

```bash
# 1. 复制上面的服务文件到 /etc/systemd/system/

# 2. 重新加载systemd
sudo systemctl daemon-reload

# 3. 配置开机自启
sudo systemctl enable adata-backend
sudo systemctl enable adata-frontend

# 4. 启动服务
sudo systemctl start adata-backend
sudo systemctl start adata-frontend
```

## 服务管理命令

```bash
# 查看状态
sudo systemctl status adata-backend
sudo systemctl status adata-frontend

# 停止服务
sudo systemctl stop adata-backend
sudo systemctl stop adata-frontend

# 启动服务
sudo systemctl start adata-backend
sudo systemctl start adata-frontend

# 重启服务
sudo systemctl restart adata-backend
sudo systemctl restart adata-frontend

# 查看日志
sudo journalctl -u adata-backend -f
sudo journalctl -u adata-frontend -f

# 禁用开机自启
sudo systemctl disable adata-backend
sudo systemctl disable adata-frontend
```

## 卸载

```bash
# 停止并禁用服务
sudo systemctl stop adata-backend adata-frontend
sudo systemctl disable adata-backend adata-frontend

# 删除服务文件
sudo rm /etc/systemd/system/adata-backend.service
sudo rm /etc/systemd/system/adata-frontend.service

# 重新加载
sudo systemctl daemon-reload
```
