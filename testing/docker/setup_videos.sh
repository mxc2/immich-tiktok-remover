#!/bin/bash

# Copy video files onto immich container
docker exec immich_server bash -c "mkdir -p /usr/src/app/videos"

docker ps

docker cp ./testing/docker/tiktok_videos immich_server:/usr/src/app/videos
docker cp ./testing/docker/non-tiktok_videos immich_server:/usr/src/app/videos

sleep 20

docker exec immich_server bash -c "ls /usr/src/app/videos"

# Upload video files to immich via the CLI

docker exec immich_server bash -c "immich login http://immich_server:2283/api sHXdxnG2xoPNveGqJI8nZSlwTEMTFvILHqzCRFyfz4 && sleep 10 && immich upload --recursive /usr/src/app/videos/tiktok_videos"
docker exec immich_server bash -c "immich login http://immich_server:2283/api sHXdxnG2xoPNveGqJI8nZSlwTEMTFvILHqzCRFyfz4 && sleep 10 && immich upload --recursive /usr/src/app/videos/non-tiktok_videos"