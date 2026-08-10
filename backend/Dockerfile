# ==================== 构建阶段 ====================
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装系统依赖（bcrypt需要gcc）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖到虚拟环境
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==================== 开发阶段 ====================
FROM python:3.11-slim AS development

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ==================== 生产阶段 ====================
FROM python:3.11-slim AS production

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN mkdir -p /app/logs

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# MVP fix: 游戏状态存内存，必须单 worker（--workers 1）；默认端口 5000，支持 $PORT 环境变量
ENV PORT=5000
EXPOSE 5000

# 使用shell形式而非JSON数组，这样 $PORT 会被正确展开
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-5000} --workers 1
