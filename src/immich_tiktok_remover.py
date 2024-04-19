"""
Script for processing video files from Immich, detecting TikTok videos, and performing actions based on configuration.

This script performs the following tasks:
1. Checks if it's the first time running the script and performs initial setup if necessary.
2. Retrieves configuration parameters.
3. Retrieves all video files from Immich.
4. Processes each video, checking if it's a TikTok video based on its name and creation date.
5. Archives or trashes TikTok videos based on configuration.
6. Outputs the results including the total number of videos processed, TikTok videos detected, total file size of TikTok videos, and any failed videos.
7. Calculates and outputs the elapsed time for the entire process.
"""

import sys
import time
import os
from image_verification import processVideo, verifyVideoNameAndDate
from immich import pingServer, getAllAssets, serveVideo, trashVideo, archiveVideo
from python_params import get_config_params
from first_time_run import firstIntroductionLines, firstTimeRunning

# Check if first time running
if not os.path.isfile('.env'):
    firstIntroductionLines()
    firstTimeRunning()
else:
    # Check if the server is reachable
    try:
        pingServer()
    except Exception as e:
        print("Error while trying to connect to Immich. Mabey delete .env file from directory and run script again?")
        sys.exit()

# Get the configuration parameters
config = get_config_params()

detectedTikTokVideos = 0
noTiktokVideos = 0
totalTikTokFileSize = 0
failedVideos = []

# Start timer for performance measurement
start_time = time.time()

# Get all files from Immich
print("Getting all video files from Immich...")
immichFiles = getAllAssets()

# Sort here for only videos, as API itself does not seems to support it
immichVideos = [file for file in immichFiles if file.get("type") == "VIDEO"]

print("Processing videos. This may take a while... \n")
if not config["outputAllVideos"]:
    print("Note: Outputting only the filenames of videos detected as TikTok videos. Overridable with --output-all flag. \n")

# Process the videos
for video in immichVideos:
    videoId = video.get("id")
    if verifyVideoNameAndDate(video.get("originalFileName"), video.get("fileCreatedAt")):
        is_tiktok = processVideo(serveVideo(videoId))
        if is_tiktok == 1:
            detectedTikTokVideos += 1
            totalTikTokFileSize += int(video.get("exifInfo").get("fileSizeInByte"))
            print(f"{video.get('originalFileName')} is a TikTok video.")
            if config["archiveVideos"]:
                archiveVideo(videoId)
            else:
                trashVideo(videoId)
            continue
        elif is_tiktok == 0 and config["outputAllVideos"]:
            print(f"{video.get('originalFileName')} is not a TikTok video.")
        elif is_tiktok == -1:
            failedVideos.append(video.get('originalFileName'))
    noTiktokVideos += 1

# Output results
totalTikTokFileSizeMB = totalTikTokFileSize / (1024 ** 2)
print(f"\n\033[1;32;40mTotal videos: {detectedTikTokVideos + noTiktokVideos}")
print(f"\033[1;32;40mFrom those, {detectedTikTokVideos} were detected as TikTok videos and {noTiktokVideos} were detected as non-TikTok videos.")
print(f"\033[1;32;40mTotal file size of TikTok videos: {totalTikTokFileSizeMB:.2f} MB.")

# Output failed videos
if len(failedVideos) > 0:
    print("\n\033[1;31;40mThe following videos failed to process:")
    for video in failedVideos:
        print(video)
    print("You can trash/archive them manually or try running the script again.\n")

# Calculate elapsed time
end_time = time.time()
elapsed_time = (end_time - start_time) / 60

print("\033[1;32;40m-" * 50)
print(f"\033[1;32;40mTime taken: {elapsed_time:.0f} minutes")
print("\033[0m")