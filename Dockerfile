FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat-traditional postgresql-client && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' django_user

COPY . .

RUN mkdir -p /code/staticfiles \
    && chown -R django_user:django_user /code \
    && chmod -R 755 /code \
    && chmod +x /code/scripts_docker/prod/run_web.sh

USER django_user
