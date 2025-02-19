FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY . .

# Установка зависимостей Python
RUN pip install --no-cache-dir -e .

# Установка дополнительных зависимостей
RUN pip install --no-cache-dir uvicorn

# Установка переменных окружения по умолчанию
ENV BR_BOT_HOST=0.0.0.0
ENV BR_BOT_PORT=8000

# Запуск API сервера
CMD ["python", "main.py"]
