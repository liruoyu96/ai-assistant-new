FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY app/ .
COPY config/.env .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 生成SSL证书
RUN openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365 \
    -subj "/C=CN/ST=State/L=City/O=Organization/CN=localhost"

# 设置权限
RUN chmod 600 key.pem cert.pem

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"] 