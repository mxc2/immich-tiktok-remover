import time
import os
from image_verification import processVideo, verifyVideoNameAndDate
from immich import getAllAssets, serveVideo, trashVideo, archiveVideo
from python_params import get_config_params
from first_time_run import firstTimeRunning

# Check if first time running
if (not os.path.isfile('.env')):
    firstTimeRunning()

# Get the configuration parameters
config = get_config_params()

detectedTikTokVideos = 0
noTiktokVideos = 0
totalTikTokFileSize = 0

# Start timer for performance measurement
start_time = time.time()

# Get all files from Immich
print("Getting all video files from Immich...")
immichVideos = getAllAssets()

# Process the videos
print("Processing videos. This may take a while...")
if (not config["outputAllVideos"]):
    print("Note: Outputting only the filenames of videos detected as TikTok videos. Overridable with --output-all flag, but that is not recommended as it will excessively spam the console. \n \n")

for video in immichVideos:
    videoId = video.get("id")
    if (not video.get("isArchived") and verifyVideoNameAndDate(video.get("originalFileName"), video.get("fileCreatedAt"))):
        tiktok_file_size = processVideo(serveVideo(videoId))
        if tiktok_file_size:
            detectedTikTokVideos += 1
            totalTikTokFileSize += tiktok_file_size
            print(f"{video.get('originalFileName')} is a TikTok video.")
            if config["archiveVideos"]:
                archiveVideo(videoId)
            else:
                trashVideo(videoId)
            continue
        elif (tiktok_file_size == 0 and config["outputAllVideos"]):
            print(f"{video.get('originalFileName')} is not a TikTok video.")
    noTiktokVideos += 1

# Output results
totalTikTokFileSizeGB = totalTikTokFileSize / (1024 ** 3)
print(f"\n\033[1;32;40mTotal videos: {detectedTikTokVideos + noTiktokVideos}")
print(f"\033[1;32;40mFrom those, {detectedTikTokVideos} were detected as TikTok videos and {noTiktokVideos} were detected as non-TikTok videos.")
print(f"\033[1;32;40mTotal file size of TikTok videos: {totalTikTokFileSizeGB:.2f} GB.")

# Calculate elapsed time
end_time = time.time()
elapsed_time = (end_time - start_time) / 60

print("-" * 50)
print(f"Time taken: {elapsed_time:.0f} minutes")