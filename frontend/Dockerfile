FROM python:3.12-slim

# Установка рабочей директории
WORKDIR /app

# Копируем pyproject.toml
COPY pyproject.toml .

RUN pip install uv

# Копируем остальной код
COPY . .

# Запуск FastAPI-приложения
# CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
