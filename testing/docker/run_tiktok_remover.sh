sed -i -e 's|https://immich.yourserver.co.uk|http://immich_server:2283|' docker-compose.yml
sed -i -e 's|your-immich-api-key|sHXdxnG2xoPNveGqJI8nZSlwTEMTFvILHqzCRFyfz4|' docker-compose.yml
sed -i '/^  immich-tiktok-remover:/a\    networks:\n      - immich_default' docker-compose.yml
echo -e "\nnetworks:\n  immich_default:\n    external: true" >> docker-compose.yml
docker compose pull
docker compose up -d