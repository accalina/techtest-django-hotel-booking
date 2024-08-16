# Preparing Stage
FROM python:3.8-alpine as base
LABEL author="Accalina"

# Builder Stage
FROM base as builder
WORKDIR /hotel
ENV PATH=/install/bin:$PATH

RUN mkdir /install
RUN apk update && apk add gcc python3-dev musl-dev

COPY config config
COPY src src
COPY manage.py .
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

# Runtime Stage
FROM base as runtime
WORKDIR /hotel
ENV PYTHONUNBUFFERED 1

# Fix Vulnerability on Kernel Filesystem
RUN apk update
RUN apk --no-cache add libpq
RUN apk --no-cache add expat
RUN apk --no-cache add libtirpc
RUN apk --no-cache add xz-libs
RUN apk --no-cache add zlib
RUN apk --no-cache add libtirpc-conf
RUN apk --no-cache add krb5-libs
RUN apk --no-cache add libcom_err
RUN apk --no-cache add ncurses-libs

# Fix Vulnerability on Pip and Python Core
RUN pip install setuptools==65.5.1 wheel==0.38.1

# add nginx for static serve
RUN apk add --no-cache nginx
RUN mkdir -p /usr/share/nginx/
RUN mkdir -p /etc/nginx/conf.d/
RUN echo -e "ENV=dev\nSECRET_KEY='THISISDUMMYSECRETKEY'\nWHITELIST_HOSTS=localhost" >> .env

COPY --from=builder /hotel .
COPY --from=builder /install /usr/local
RUN python manage.py collectstatic --noinput
RUN mv ./static /usr/share/nginx/html
RUN echo 'server { listen 80; location / { root /usr/share/nginx/html; try_files $uri $uri/ =404; } }' > /etc/nginx/http.d/default.conf