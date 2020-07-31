FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8
RUN apk --update add bash nano
RUN apk add --no-cache tzdata
ENV TZ America/Detroit
ENV STATIC_URL /signageWebpage/static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt
