import os
try:
    from moviepy import VideoFileClip
    MOVIEPY_AVAILABLE = True
    MOVIEPY_ERROR = None
except ImportError as e:
    MOVIEPY_AVAILABLE = False
    MOVIEPY_ERROR = str(e)
except Exception as e:
    MOVIEPY_AVAILABLE = False
    MOVIEPY_ERROR = str(e)

def is_image(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.ico', '.tiff']

def is_video(path):
    ext = os.path.splitext(path)[1].lower()
    return ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.gif']
