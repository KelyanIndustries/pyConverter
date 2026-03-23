import os
from PIL import Image
from .utils import MOVIEPY_AVAILABLE, MOVIEPY_ERROR, is_image, is_video, VideoFileClip
from .config import FORMATS_IMAGE, FORMATS_VIDEO

def convert_file(input_path, target_ext):
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}{target_ext}"
    
    if is_image(input_path):
            img = Image.open(input_path)
            if target_ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.save(output_path)
            return output_path

    elif is_video(input_path):
        if not MOVIEPY_AVAILABLE:
                raise ImportError(f"MoviePy manquant. Détail: {MOVIEPY_ERROR or 'Inconnu'}")

        clip = VideoFileClip(input_path)
        
        try:
            if target_ext == '.gif':
                clip.write_gif(output_path, logger=None)
            elif target_ext == '.mp3':
                clip.audio.write_audiofile(output_path, logger=None)
            else:
                # Video -> Video
                codecs_map = {
                    '.mp4': {'codec': 'libx264', 'audio_codec': 'aac'},
                    '.avi': {'codec': 'mpeg4', 'audio_codec': 'libmp3lame'},
                    '.mov': {'codec': 'libx264', 'audio_codec': 'aac'},
                    '.webm': {'codec': 'libvpx', 'audio_codec': 'libvorbis'},
                    '.mkv': {'codec': 'libx264', 'audio_codec': 'aac'}
                }
                params = codecs_map.get(target_ext, {'codec': 'libx264', 'audio_codec': 'aac'})
                clip.write_videofile(output_path, codec=params['codec'], audio_codec=params['audio_codec'], logger=None)
        finally:
            clip.close()
        
        return output_path
    
    raise ValueError(f"Type de fichier non supporté ou conversion impossible: {input_path}")
