import os
from moviepy.editor import VideoFileClip
from PIL import Image
import pytesseract

def has_tiktok_watermark(video_path):
    # Check if the file is an mp4
    if not video_path.lower().endswith('.mp4'):
        return False

    # Check if the file name contains "-"
    if '-' in os.path.basename(video_path):
        return False

    # Check creation date (assuming file creation date is the same as modification date)
    if os.path.getmtime(video_path) < 1451606400:  # 1451606400 is the timestamp for Jan 1, 2016
        return False

    # Analyze the last 3 seconds of the video for the TikTok watermark
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        last_3_seconds = clip.subclip(max(0, duration - 3), duration)
        last_3_seconds.write_videofile("last_3_seconds.mp4")  # Export the last 3 seconds to a temporary file

        # 1. Use Image-to-Text
        text = pytesseract.image_to_string(Image.open("last_3_seconds.mp4"))
        if "Tik Tok" in text and "@" in text:
            print("Found TikTok watermark text:", text)
        else:
            print("No TikTok watermark text found.")

        # 2. Check Background Color
        img = Image.open("last_3_seconds.mp4")
        colors = img.getcolors(img.size[0] * img.size[1])
        dominant_color = max(colors, key=lambda x: x[0])[1]
        dominant_percentage = max(colors, key=lambda x: x[0])[0] / sum([x[0] for x in colors])
        if dominant_percentage > 0.8:
            print("Over 80% of the background is one color.")
        else:
            print("Background color is not dominant.")

        clip.close()
        return True  # Return True if any of the conditions are met
    except Exception as e:
        print("Error processing video:", e)
        return False
    finally:
        # Clean up temporary files
        if os.path.exists("last_3_seconds.mp4"):
            os.remove("last_3_seconds.mp4")

# Example usage
video_path = "path/to/your/video.mp4"
if has_tiktok_watermark(video_path):
    print("This is a TikTok video.")
else:
    print("This is not a TikTok video.")
