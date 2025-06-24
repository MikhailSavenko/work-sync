#!/bin/bash

# Ждем, пока база данных будет доступна
until nc -z db 5432; do
  echo "Ожидание базы данных..."
  sleep 1
done

# Создаем миграции
echo "Применение миграций..."
python manage.py makemigrations

# Применяем миграции
echo "Применение миграций..."
python manage.py migrate

# Наполним базу товарами
echo "Наполняем базу товарами..."


# Запускаем приложение
echo "Запуск приложения..."
gunicorn work_sync.wsgi:application --bind 0.0.0.0:8000 --log-level info

