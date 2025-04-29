#!/bin/sh

# 避免資料庫還沒準備好
echo "等待資料庫啟動..."
sleep 5

# 執行數據庫遷移
echo "執行數據庫遷移..."
python manage.py migrate

# 收集靜態文件（如果有需要）
echo "收集靜態文件..."
python manage.py collectstatic --noinput

# 啟動 Gunicorn
echo "啟動 Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 storage.wsgi:application
