from enum import Enum
from datetime import datetime
from background_task import background
from moviepy.editor import VideoFileClip
from .settings import MEDIA_ROOT
from os import path, mkdir
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video import fx
# import os
# from .settings import MEDIA_ROOT, MEDIA_URL
# from pyffmpeg import FFmpeg

class Globals:
        class Gender(Enum):
                MALE = 1
                FEMALE = 2
                ENBY = 3
                ANY = 4
                NONE = 404
                def Encode(nem):
                        for gender in Globals.Gender.__members__.values():
                                if gender.name.upper() == nem.upper():
                                        return gender.value
                        else:return Globals.Gender.NONE.value
                
                def Decode(code):
                        if code == 1:
                                return "MALE"
                        elif code == 2:
                                return "FEMALE"
                        elif code == 3:
                                return "ENBY"
                        elif code == 4:
                                return "ANY"
                        elif code == 404:
                                return "NONE"
                        else:
                                return "UNKNOWN"


        def deconstruct(object:object, attribute:str, sep:str):
                """
                object: object the object you desire to work on
                attribute: str the attribute of the object you want to use
                sep: str the separator, at which the returned value is split
                """
                if sep is not None:
                        return getattr(object, attribute).split(sep)
                return getattr(object, attribute).split(";")


        def formatDate(input_string):
                print(input_string)
                try:
                        input_date = datetime.strptime(input_string, "%Y. %m. %d.").date()
                except ValueError:
                        input_date = datetime.strptime(input_string, "%Y/%m/%d").date()
                
                formatted_date = input_date.strftime("%Y-%m-%d")
                return formatted_date

        #@background(schedule=200)
        def generate_thumbnail(video_path, title, user, video):
                from .models import ThumbnailModel

                # Load the video clip
                clip = VideoFileClip(video_path)
                clip = clip.subclip(0,2)
                # Set the time (in seconds) for the thumbnail
                thumbnail_time = 1

                # Save the thumbnail as an image file
                outf = MEDIA_ROOT + f'/thumbnail/{title}.jpg'  # Replace with your desired file path and name
                directory_path = path.join(MEDIA_ROOT, 'thumbnail/')
                if path.exists(directory_path) == False and path.isdir(directory_path) ==False:
                        mkdir(directory_path)
                # Generate the thumbnail by selecting a frame at the specified time
                thumbnail_frame = clip.save_frame(outf,t=thumbnail_time)

                # Save the thumbnail path to the database
                thumbnail = ThumbnailModel(user=user, thumbnail=outf, relatedvideo=video)
                thumbnail.save()
