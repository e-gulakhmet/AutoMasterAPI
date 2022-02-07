###########
# BUILDER #
###########
FROM python:3.10-buster

LABEL maintainer="Enes Gulakhmet <wwho.mann.3@gmail.com>"

RUN apt-get update -y && apt-get install -y netcat

# create the appropriate directories
ENV HOME=/usr/src/app
WORKDIR $HOME

ARG DJANGO_SECRET_KEY="DJANGO_SECRET_KEY"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . $HOME

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV STATIC_URL /static
ENV STATIC_PATH static

ENV MEDIA_URL /media
ENV MEDIA_PATH media

RUN python manage.py collectstatic

EXPOSE 80

HEALTHCHECK --interval=12s --timeout=12s --start-period=10s \
 CMD curl --fail http://localhost/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
