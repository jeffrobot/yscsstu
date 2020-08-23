FROM python:3.7-slim AS builder
WORKDIR /code

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
        build-essential \
        default-libmysqlclient-dev \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN set -ex \
    && python -m venv /venv \
    && bash -c ': \
    && source /venv/bin/activate \
    && set -ex \
    && pip install -r requirements.txt'

COPY . ./
RUN rm id_rsa

FROM python:3.7-slim
WORKDIR /code

RUN set -ex \
    && apt-get update \
    && apt-get install -y \
      build-essential \
      default-libmysqlclient-dev \
      nginx \
      supervisor \
    && rm -rf /var/lib/apt/lists/* \
    && echo "\ndaemon off;" >> /etc/nginx/nginx.conf \
    && rm /etc/nginx/sites-enabled/default \
    && chown -R www-data:www-data /var/lib/nginx \
    && ln -sf /code/nginx-app.conf /etc/nginx/sites-enabled/ \
    && ln -sf /code/supervisor-app.conf /etc/supervisor/conf.d/ \
    && sed -i -e 's#access_log /var/log/nginx/access.log;#access_log off;#' /etc/nginx/nginx.conf

COPY --from=builder /venv /venv
COPY --from=builder /code /code
CMD ["bash", "-c", "source /venv/bin/activate && supervisord -n"]
