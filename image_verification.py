import os
import numpy as np
import easyocr
import tempfile
from moviepy.editor import VideoFileClip
from datetime import datetime
from python_params import get_config_params

def getRandomFrame(clip):
    duration = clip.duration
    random_time = np.random.uniform(0, duration)  # Generate a random time within the duration
    return clip.get_frame(random_time)  # Extract frame at the random time

def getFrameFromEnd(clip):
    duration = clip.duration
    return clip.get_frame(duration - 1)  # Extract frame at the specified time

# Currently not used
# def checkVideoStereo(clip):
#     return clip.audio.nchannels <= 2

def extractFrame(video_path, frameFunction):
    clip = VideoFileClip(video_path)
    frame = frameFunction(clip)
    
    # Close the clip to release resources
    clip.close()
    
    return frame

def checkForWatermarkInVideo(frame):
    reader = easyocr.Reader(['en'])
    result = str(reader.readtext(frame))
    if "TikTok" in result:
        return True
    return False

def verifyVideoNameAndDate(file_name, created_at):
    config = get_config_params()

    # Check file extension
    if not file_name.lower().endswith(tuple(config["fileTypesToCheckFor"])):
        return False
    
    # Check file name length
    if len(file_name) != config["fileNameLength"]: return False

    # Check the video creation date
    video_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    timestamp = video_date.timestamp()

    if timestamp < config["fileCreatedAfter"]:
        return False
    return True

def hasTiktokWatermark(video_path):
    totalFileSize = 0  # Initialize total file size

    # Get the file size
    file_size = os.path.getsize(video_path)

    # Extract a single frame from the near end of the video
    frame = extractFrame(video_path, getFrameFromEnd)
    if (checkForWatermarkInVideo(frame)):
        totalFileSize += file_size

    # If first check failed, redo test but with a random frame now
    frame = extractFrame(video_path, getRandomFrame)
    if (checkForWatermarkInVideo(frame)):
        totalFileSize += file_size

    return totalFileSize
    
def processVideo(video_content):
    # Save video content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_content)
        temp_file_path = temp_file.name
    
    try:        
        # Process the video using has_tiktok_watermark function
        tiktok_file_size = hasTiktokWatermark(temp_file_path)
    except Exception as e:
        print("Error processing video:", e)

    # Delete the temporary file
    os.unlink(temp_file_path)
    
    return tiktok_file_size 
