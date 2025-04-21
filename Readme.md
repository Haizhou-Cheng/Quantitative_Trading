Welcome and Test

Create Environement:
D:\CHZ\micromamba\micromamba.exe activate quant create -n quant python=3.10
D:\CHZ\micromamba\micromamba.exe activate quant activate quant


pip install jupyterlab numpy pandas scipy matplotlib seaborn
pip install ta-lib pyarrow psycopg2-binary

pip install backtrader zipline-reloaded vectorbt
pip install ccxt requests-cache aiohttp

Install extension:
Python Pylance
Jupyter
Docker
Remote - SSH

Create .vscode file in your workspace and create setting.json file:
{
  "python.linting.mypyEnabled": true,
  "jupyter.notebookFileRoot": "${workspaceFolder}/research",
  "python.analysis.typeCheckingMode": "strict"
}

# 安装 SSH 服务器
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
# 启动 SSH 服务
Start-Service sshd
# 设置为开机自启
Set-Service -Name sshd -StartupType 'Automatic'

netstat -an | findstr :22

ipconfig

IPv4 地址: 192.168.3.28

Ctrl+Shift+P
Remote-SSH: Add New SSH Host

ssh your_username@IPv4
ssh Admin@192.168.3.28