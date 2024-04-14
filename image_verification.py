import os
import numpy as np
import easyocr
import tempfile
from moviepy.editor import VideoFileClip
from datetime import datetime
from python_params import get_config_params

config = get_config_params()

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
    try:
        clip = VideoFileClip(video_path)
        frame = frameFunction(clip)
        return frame
    finally:
        clip.close()

def checkForWatermarkInVideo(frame):
    reader = easyocr.Reader(['en'])
    result = str(reader.readtext(frame))
    if config["textToCheckFor"] in result:
        return True
    
    return False

def verifyVideoNameAndDate(file_name, created_at):
    # Check file extension
    if len(config["fileTypesToCheckFor"]) != 0 and not file_name.lower().endswith(tuple(config["fileTypesToCheckFor"])):
        return False
    
    # Check file name length without extension
    name_without_extension = ""
    if config["fileNameLength"] != 0:
        last_dot_index = file_name.rfind('.')
        if last_dot_index != -1:
            name_without_extension = file_name[:last_dot_index]
        else:
            name_without_extension = file_name
        if len(name_without_extension) != config["fileNameLength"]:
            return False
        
    # Check if file name contains of only letters and numbers
    if config["fileNameIsAlumn"] != False and not name_without_extension.isalnum(): return False

    # Check the video creation date
    if config["fileCreatedAfter"] != 0:
        video_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        timestamp = video_date.timestamp()

        if timestamp < config["fileCreatedAfter"]:
            return False  
    return True

def hasTiktokWatermark(video_path):
    # Extract a single frame from the near end of the video
    frame = extractFrame(video_path, getFrameFromEnd)
    if (checkForWatermarkInVideo(frame)):
        return 1

    # If first check failed, redo test but with a random frame now
    frame = extractFrame(video_path, getRandomFrame)
    if (checkForWatermarkInVideo(frame)):
        return 1

    return 0
    
def processVideo(video_content):
    # Save video content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(video_content)
        temp_file_path = temp_file.name
    
    # is_tiktok would be better as a boolean, might fix in future
    try:        
        # Process the video using has_tiktok_watermark function
        is_tiktok = hasTiktokWatermark(temp_file_path)
    except Exception as e:
        print("Error processing video:", e)
        is_tiktok = -1

    # Delete the temporary file
    os.unlink(temp_file_path)
    
    return is_tiktok
