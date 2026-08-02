# ==================== 构建阶段 ====================
FROM python:3.11-slim AS builder

WORKDIR /app

# 安装系统依赖
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

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制虚拟环境（包含所有依赖）
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动开发服务器
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

# ==================== 生产阶段 ====================
FROM python:3.11-slim AS production

WORKDIR /app

# 安装系统依赖（仅运行时需要）
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制虚拟环境（包含所有依赖）
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制源代码
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 创建非root用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 5000

# 启动生产服务器
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]
