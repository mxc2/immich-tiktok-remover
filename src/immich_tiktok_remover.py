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
from image_verification import processVideo, verifyVideoNameAndDate, verifyImageNameAndDate, processImage
from immich import pingServer, getAllAssets, serveVideo, serveImage, trashAsset, archiveAsset, getVideoAdditionalData
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
        print("Error while trying to connect to Immich. Maybe delete the .env file from the working directory and run script again?")
        sys.exit()

# Get the configuration parameters
config = get_config_params()

detectedTikTokImages = 0
detectedTikTokVideos = 0

noTikTokImages = 0
noTiktokVideos = 0

totalTikTokFileSize = 0

failedVideos = []
failedImages = []

# Start timer for performance measurement
start_time = time.time()

# Get all files from Immich

print("Getting all video files from Immich...")
immichVideos = getAllAssets("VIDEO")

if config["checkForTikTokImages"]:
    print("Getting all images from Immich...")
    immichImages = getAllAssets("IMAGE")

print("Processing assets. This may take a while... \n")
if not config["outputAllVideos"]:
    print("Note: Outputting only the filenames of videos detected as TikTok videos. Overridable with --output-all flag. \n")

# Process the videos
for video in immichVideos:
    videoId = video.get("id")
    if verifyVideoNameAndDate(video.get("originalFileName"), video.get("fileCreatedAt")):
        try:
            is_tiktok = processVideo(serveVideo(videoId))
        except:
            is_tiktok = -1
        if is_tiktok == 1:
            detectedTikTokVideos += 1

            videoData = getVideoAdditionalData(videoId)
            totalTikTokFileSize += int(videoData.get("exifInfo").get("fileSizeInByte"))

            print(f"{videoData.get('originalFileName')} detected as a TikTok video.")
            if config["archiveVideos"]:
                archiveAsset(videoId)
            else:
                trashAsset(videoId)
            continue
        elif is_tiktok == 0 and config["outputAllVideos"]:
            print(f"{video.get('originalFileName')} is not a TikTok video.")
        elif is_tiktok == -1:
            failedVideos.append(video.get('originalFileName'))
    noTiktokVideos += 1

if config["checkForTikTokImages"]:
    print("Processing images. This may take a while... \n")
    for image in immichImages:
        imageId = image.get("id")
        #print(imageId)
        if verifyImageNameAndDate(image.get("originalFileName"), image.get("fileCreatedAt")):
            try:
                is_tiktok = processImage(serveImage(imageId))
            except:
                is_tiktok = -1
            if is_tiktok == 1:
                detectedTikTokImages += 1

                imageData = getVideoAdditionalData(imageId)
                totalTikTokFileSize += int(imageData.get("exifInfo").get("fileSizeInByte"))

                print(f"{imageData.get('originalFileName')} detected as a TikTok image.")
                if config["archiveVideos"]:
                    archiveAsset(imageId)
                else:
                    trashAsset(imageId)
                continue
            elif is_tiktok == 0 and config["outputAllVideos"]:
                print(f"{image.get('originalFileName')} is not a TikTok video.")
            elif is_tiktok == -1:
                failedImages.append(image.get('originalFileName'))
        noTikTokImages += 1

# Output results
totalTikTokFileSizeMB = totalTikTokFileSize / (1024 ** 2)
print(f"\n\033[1;32;40mTotal videos: {detectedTikTokVideos + noTiktokVideos}")
print(f"\033[1;32;40mFrom those, {detectedTikTokVideos} were detected as TikTok videos and {noTiktokVideos} were detected as non-TikTok videos.")
if config["checkForTikTokImages"]:
    print(f"\n\033[1;32;40mTotal images: {detectedTikTokImages + noTikTokImages}")
    print(f"\033[1;32;40mFrom those, {detectedTikTokImages} were detected as TikTok images and {noTikTokImages} were detected as non-TikTok images.")
print(f"\n\033[1;32;40mTotal file size of TikTok assets: {totalTikTokFileSizeMB:.2f} MB.")

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