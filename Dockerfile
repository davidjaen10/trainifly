FROM python:3.10
ENV PYTHONUNBUFFERED = 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' django_user
COPY . /code/

# Crear carpeta staticfiles con permisos correctos
RUN mkdir -p /code/staticfiles && chown -R django_user:django_user /code/staticfiles && chmod -R 755 /code/staticfiles
RUN chown -R django_user:django_user /code && chmod -R 755 /code
