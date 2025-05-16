# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск бота
CMD ["python", "bot/main.py"]

