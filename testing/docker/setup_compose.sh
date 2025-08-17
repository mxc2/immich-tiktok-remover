#!/bin/bash

mkdir tmp

chmod -R +rw ./testing/docker/templates

cp ./testing/docker/templates/env-template tmp/.env

cp /etc/localtime tmp/time

cd tmp

wget -O docker-compose.yml https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml

sed -i -e 's/-\ \/etc\/localtime/\-\ .\/time/g' docker-compose.yml

docker compose up -d

sleep 10