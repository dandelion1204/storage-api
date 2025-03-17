# 使用官方 Python 3.9 的輕量版映像
FROM python:3.9-slim

# 更新系統並安裝 Pillow 需要的依賴
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    libtiff-dev \
    libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

# 設定容器內的工作目錄
WORKDIR /storage

# 複製專案所有文件到容器內
COPY . /storage/

# 安裝系統依賴（如果需要使用 PostgreSQL，則保留 libpq-dev）
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*



# 安裝 Python 依賴（確保 `requirements.txt` 存在）
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Django 的預設 HTTP 端口
EXPOSE 8000

# 讓 Django 先執行 migrate 再啟動
#ENTRYPOINT ["sh", "-c"]
#CMD ["python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

#ENTRYPOINT ["sh", "-c", "python manage.py migrate"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

ENTRYPOINT ["sh", "-c", "
    python manage.py migrate && \
    exec gunicorn --bind 0.0.0.0:8000 storage.wsgi:application
"]

