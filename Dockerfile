# Dockerfile

FROM python:3.9-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "workmate_task.wsgi:application", "--bind", "0.0.0.0:8000"]
