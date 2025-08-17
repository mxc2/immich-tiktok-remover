#!/bin/bash

sleep 60 # Give time for the tool to run

docker logs immich-tiktok-remover

expected_count=$(find ./testing/docker/tiktok_videos -type f | wc -l)

log_output=$(docker logs immich-tiktok-remover 2>&1 | grep 'were detected as TikTok videos' | tail -n 1)

# If no matching line was found
if [[ -z "$log_output" ]]; then
    echo "Error: No matching log line found."
    exit 2
fi

# Extract only the first number before "were detected as TikTok videos"
detected_count=$(echo "$log_output" | awk '{ for(i=1;i<=NF;i++) if ($i=="were" && $(i-1) ~ /^[0-9]+$/) { print $(i-1); exit } }' | tr -d '\r' | xargs)

# Check if the number matches the expected count
if [[ "$detected_count" -eq "$expected_count" ]]; then
    echo "Success: $detected_count TikTok videos detected, $expected_count files found."
    exit 0
else
    echo "Fail: $detected_count TikTok videos detected, but $expected_count files found."
    exit 1
fi
