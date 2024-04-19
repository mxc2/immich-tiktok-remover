"""
This module contains functions to verify if a video contains a TikTok watermark.
It uses the EasyOCR library to perform OCR on the video frames and check for the watermark.
"""

import os
import tempfile
from datetime import datetime
from typing import Callable
import numpy as np
import easyocr
from moviepy.editor import VideoFileClip
from python_params import get_config_params

config = get_config_params()

def getRandomFrame(clip: VideoFileClip):
    """
    Returns a randomly selected frame from the given video clip.
    """
    duration = clip.duration
    random_time = np.random.uniform(0, duration)  # Generate a random time within the duration
    return clip.get_frame(random_time)  # Extract frame at the random time

def getFrameFromEnd(clip: VideoFileClip):
    """
    Returns the frame from the end of the given video clip.
    """
    duration = clip.duration
    return clip.get_frame(duration - 1)  # Extract frame at the specified time

def extractFrame(video_path: str, frameFunction: Callable[[VideoFileClip], np.ndarray]):
    """
    Extracts a frame from a video using the provided frame extraction function.
    """
    try:
        clip = VideoFileClip(video_path)
        frame = frameFunction(clip)
        return frame
    finally:
        clip.close()

def checkForWatermarkInVideo(frame: np.ndarray):
    """
    Checks if a watermark is present in the given frame using OCR.
    """
    reader = easyocr.Reader(['en'])
    result = str(reader.readtext(frame))
    if config["textToCheckFor"] in result:
        return True

    return False

def verifyVideoNameAndDate(file_name: str, created_at: str):
    """
    Verifies the name and creation date of a video file based on configured parameters.
    """
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
    is_alnum = name_without_extension.isalnum()
    if config["fileNameIsAlumn"] != False and not is_alnum: return False

    # Check the video creation date
    if config["fileCreatedAfter"] != 0:
        video_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        timestamp = video_date.timestamp()

        if timestamp < config["fileCreatedAfter"]:
            return False
    return True

def hasTiktokWatermark(video_path: str):
    """
    Checks if a TikTok watermark is present in the given video. 
    Failing to find the watermark in the first frame, it will try a random frame.
    """
    # Extract a single frame from the near end of the video
    frame = extractFrame(video_path, getFrameFromEnd)
    if checkForWatermarkInVideo(frame):
        return 1

    # If first check failed, redo test but with a random frame now
    frame = extractFrame(video_path, getRandomFrame)
    if checkForWatermarkInVideo(frame):
        return 1

    return 0

def processVideo(video_content: bytes):
    """
    Processes the given video content to determine if it contains a TikTok watermark.
    Failing to process the video will return -1.
    """
    if not config.get("avoidImageRecognition"):
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
    else:
        # Skip image recognition for archiving/deletion. Return 1 as default.
        return 1
