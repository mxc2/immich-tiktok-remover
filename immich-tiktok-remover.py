import time
import os
from image_verification import processVideo, verifyVideoNameAndDate
from immich import getAllAssets, serveVideo, trashVideo, archiveVideo
from python_params import get_config_params
from first_time_run import firstIntroductionLines, firstTimeRunning

# Check if first time running
if (not os.path.isfile('.env')):
    firstIntroductionLines()
    firstTimeRunning()

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
immichVideos = getAllAssets()

print("Processing videos. This may take a while...")
if (not config["outputAllVideos"]):
    print("Note: Outputting only the filenames of videos detected as TikTok videos. Overridable with --output-all flag. \n \n")

# Process the videos
for video in immichVideos:
    videoId = video.get("id")
    if (verifyVideoNameAndDate(video.get("originalFileName"), video.get("fileCreatedAt"))):
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
        else:
            failedVideos.append(video.get('originalFileName'))
    noTiktokVideos += 1

# Output results TODO: Currently outputs videos
totalTikTokFileSizeGB = totalTikTokFileSize / (1024 ** 3)
print(f"\n\033[1;32;40mTotal videos: {detectedTikTokVideos + noTiktokVideos}")
print(f"\033[1;32;40mFrom those, {detectedTikTokVideos} were detected as TikTok videos and {noTiktokVideos} were detected as non-TikTok videos.")
print(f"\033[1;32;40mTotal file size of TikTok videos: {totalTikTokFileSizeGB:.2f} GB.")

# Output failed videos
if (len(failedVideos) > 0):
    print("\n\033[1;31;40mThe following videos failed to process:")
    for video in failedVideos:
        print(video)
    print("You can trash/archive them manually or try running the script again.\n")

# Calculate elapsed time
end_time = time.time()
elapsed_time = (end_time - start_time) / 60

print("\033[1;32;40m-" * 50)
print(f"\033[1;32;40mTime taken: {elapsed_time:.0f} minutes")