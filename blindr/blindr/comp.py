from background_task import background
from moviepy.editor import VideoFileClip
from .settings import MEDIA_ROOT
from asgiref.sync import sync_to_async, async_to_sync


def calculate_bitrate(duration, size):
    #Bitrate = file size / (number of minutes * .0075).
    bitrate = size / ((duration/60)*0.0075)
    return bitrate

def compress(file, filename):
    """
        file:file
        filename:string
    """
    import sys
    from subprocess import run, PIPE
    from pathlib import Path

    args = sys.argv[1:]
    video_file = Path(' '.join(args))
    print("_____________________", 'ffmpeg', '-i', file, '-vcodec', 'h264', '-acodec','aac', file.replace('.' + file.split('.')[-1], '-compressed.' + file.split('.')[-1]))
    run(['ffmpeg', '-i', video_file.name, '-vcodec', 'h264', '-acodec','aac', video_file.name.replace('.' + video_file.name.split('.')[-1], '-compressed.' + video_file.name.split('.')[-1])])