# ==================== 构建阶段 ====================
FROM node:18-alpine AS builder

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm ci

# 复制源代码
COPY . .

# 构建（默认base为根路径，可通过ARG覆盖）
ARG VITE_BASE_PATH=/
ENV VITE_BASE_PATH=$VITE_BASE_PATH
RUN npm run build

# ==================== 开发阶段 ====================
FROM node:18-alpine AS development

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖（包括开发依赖）
RUN npm install

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 5173

# 启动开发服务器
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ==================== 生产阶段 ====================
FROM nginx:alpine AS production

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
