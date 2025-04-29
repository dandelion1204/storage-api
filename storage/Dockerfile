# 使用官方 Python 映像
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製專案文件
COPY requirements.txt .

# 安裝相依套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製 Django 專案
COPY . .

# 收集靜態檔案
RUN python manage.py collectstatic --noinput

# 透過 Gunicorn 啟動 Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "storage.wsgi:application"]