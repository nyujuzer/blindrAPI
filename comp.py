from moviepy.editor import VideoFileClip
from .settings import MEDIA_ROOT

def calculate_bitrate(duration, size):
    #Bitrate = file size / (number of minutes * .0075).
    bitrate = size / ((duration/60)*0.0075)
    return bitrate

def compress(file, filename):
    """
        file:file
        filename:string
    """
    video_clip = VideoFileClip(file)
    output_file = f'{MEDIA_ROOT}/videos/{filename}-compressed.mp4'
    desired_filesize = 100
    duration = video_clip.duration
    calculated_bitrate = calculate_bitrate(duration, desired_filesize)
    target_Bitrate = f'{calculated_bitrate}k'
    video_clip = video_clip.resize(newsize=(1080, 1920))
    video_clip.write_videofile(output_file, codec='libx264', bitrate=target_Bitrate)
    print("successfully wrote output file")
    print(f'media/videos/{filename}.compressed.mp4')
    return f'/videos/{filename}-compressed.mp4'