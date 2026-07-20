快速启动（本地开发）

1. 创建虚拟环境并安装依赖：
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
2. 直接运行（使用内置 SQLite）：
   uvicorn app.main:app --reload --port 8000
3. 或使用 docker-compose（切换到 Postgres）：
   cp .env.example .env
   docker-compose up --build

重要：示例为合规演示。不包含任何自动化登录或抓取未经授权站点的代码。若获得目标平台授权，我们可替换模拟适配器为真实 API 适配器。
