#!/bin/bash

cat docker-compose.yml

echo && echo
echo "The above is the contents of docker-compose.yml, if you want to change the tag or environment variables for testing, please do so before running this script. Do not change the URL or API key as these are set by the test"
echo

read -p "These tests should not be run in a live environment where you have Immich running. Continue? (Y/N) > " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo cp docker-compose.yml docker-compose-backup.yml
    sudo ./testing/docker/setup_time.sh
    sudo ./testing/docker/setup_compose.sh
    sudo ./testing/docker/restore_db.sh
    sudo ./testing/docker/setup_videos.sh
    sudo ./testing/docker/run_tiktok_remover.sh
    sudo ./testing/docker/check_itr_output.sh
    sudo mv docker-compose-backup.yml docker-compose.yml
    sudo ./testing/docker/cleanup.sh 2>/dev/null
fi

echo
read -p "Do you want to test the lite version of this tool? (Y/N) > " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo cp docker-compose.yml docker-compose-backup.yml
    sudo ./testing/docker/setup_time.sh
    sudo ./testing/docker/setup_compose.sh
    sudo ./testing/docker/set_stable-lite.sh
    sudo ./testing/docker/restore_db.sh
    sudo ./testing/docker/setup_videos.sh
    sudo ./testing/docker/run_tiktok_remover.sh
    sudo ./testing/docker/check_itr_output.sh
    sudo mv docker-compose-backup.yml docker-compose.yml
    sudo ./testing/docker/cleanup.sh 2>/dev/null
fi