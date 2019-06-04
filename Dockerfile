FROM ubuntu

RUN mkdir -p /var/www
COPY . /var/www

WORKDIR /var/www

RUN apt-get update
RUN apt-get install -y sudo

RUN sudo apt-get install -y python3.6 \
                            python3-pip \
                            qt5-default \
                            libqt5webkit5-dev \
                            build-essential \
                            python-lxml \
                            xvfb \
                            software-properties-common \
#                            nginx

RUN apt-get update && export DJANGO_ENV=prod

RUN sudo add-apt-repository -y ppa:nginx/stable

RUN pip3 install -r requirements.txt --no-cache-dir

COPY deploy/nginx/nginx.conf /etc/nginx/nginx.conf
COPY deploy/nginx/uwsgi.ini /opt/conf/uwsgi.ini
COPY deploy/nginx/uwsgi_params /opt/conf/uwsgi_params

CMD ["/bin/bash", "-c", "deploy/scripts/docker-entrypoint.sh"]

EXPOSE 80
