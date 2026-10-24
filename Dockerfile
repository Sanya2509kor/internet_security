FROM python:3.11-slim


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Запускаем Gunicorn (замените название_проекта на ваше)
CMD ["gunicorn", "internet_security.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]