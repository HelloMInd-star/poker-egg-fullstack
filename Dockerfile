FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# 安装依赖（先复制requirements利用缓存）
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# 复制后端代码
COPY backend /app/

# Railway 注入 PORT 环境变量，默认 8000
ENV PORT=8000
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=5 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

# 直接用 exec 形式启动，sh 会展开 $PORT
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT} --workers 1"]
