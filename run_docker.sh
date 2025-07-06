#!/bin/bash

while true
do 
    python3 immich_tiktok_remover.py
    sleep $RESTART_TIMEOUT
done