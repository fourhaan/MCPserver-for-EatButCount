# MCP Server Setup Guide

This guide explains how to run the MCP server on Ubuntu as a systemd service using your virtual environment.

## Environment Template

- Project path: `/home/<your-user>/<your-project-dir>`
- Python (venv) path: `/home/<your-user>/<your-venv-dir>/bin/python`
- Service name: `<your-service-name>.service`

## 1. Create the systemd service

Create the file:

```bash
sudo nano /etc/systemd/system/<your-service-name>.service
```

Paste:

```ini
[Unit]
Description=MCP Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=<your-user>
Group=<your-user>
WorkingDirectory=/home/<your-user>/<your-project-dir>
EnvironmentFile=/home/<your-user>/<your-project-dir>/.env
ExecStart=/home/<your-user>/<your-venv-dir>/bin/python /home/<your-user>/<your-project-dir>/<your-server-file>.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

## 2. Enable and start service

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now <your-service-name>.service
```

## 3. Daily service commands

Start:

```bash
sudo systemctl start <your-service-name>.service
```

Stop:

```bash
sudo systemctl stop <your-service-name>.service
```

Restart:

```bash
sudo systemctl restart <your-service-name>.service
```

Status:

```bash
sudo systemctl status <your-service-name>.service
```

## 4. View logs

Follow live logs:

```bash
sudo journalctl -u <your-service-name>.service -f
```

Last 100 lines:

```bash
sudo journalctl -u <your-service-name>.service -n 100 --no-pager
```

## 5. Disable auto-start on boot

```bash
sudo systemctl disable <your-service-name>.service
```

Re-enable:

```bash
sudo systemctl enable <your-service-name>.service
```

## 6. Common troubleshooting

If service is stuck in restart loop:

```bash
sudo systemctl stop <your-service-name>.service
sudo systemctl reset-failed <your-service-name>.service
```

Verify python path exists:

```bash
ls -l /home/<your-user>/<your-venv-dir>/bin/python
```

Verify app can run manually:

```bash
cd /home/<your-user>/<your-project-dir>
sudo -u <your-user> /home/<your-user>/<your-venv-dir>/bin/python <your-server-file>.py
```

After fixing service file:

```bash
sudo systemctl daemon-reload
sudo systemctl restart <your-service-name>.service
```

## 7. Endpoint

Your MCP SSE endpoint is:

- `http://<server-ip>:8000/sse`

From the same Ubuntu machine:

- `http://localhost:8000/sse`
