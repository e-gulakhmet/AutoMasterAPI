###########
# BUILDER #
###########
FROM python:3.10-buster

LABEL maintainer="Enes Gulakhmet <wwho.mann.3@gmail.com>"

RUN apt-get update -y

# create the appropriate directories
ENV HOME=/usr/src/app
WORKDIR $HOME

# change it in production via build command
ARG DJANGO_SECRET_KEY="DJANGO_SECRET_KEY"
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . $APP_HOME

RUN pip install -r requirements.txt

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH static

# URL under which media (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV MEDIA_URL /media
# Absolute path in where the media files wil be
ENV MEDIA_PATH media

RUN python manage.py collectstatic

EXPOSE 80

HEALTHCHECK --interval=12s --timeout=12s --start-period=10s \
 CMD curl --fail http://localhost/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
