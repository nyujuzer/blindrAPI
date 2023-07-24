from enum import Enum
from datetime import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video import fx
import os
from .settings import MEDIA_ROOT, MEDIA_URL
from pyffmpeg import FFmpeg

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

        def generate_thumbnail(video_path, video, user):
                from .models import ThumbnailModel

                inf = video_path
                outf = MEDIA_ROOT + '/thumbnail/test.jpg'

                ff = FFmpeg()
                try:

                        ff.convert(inf, outf)
                except:
                        print("self - error")
                # Save the thumbnail to the database
                thumbnail = ThumbnailModel(user=user,thumbnail = outf, relatedvideo=video)
                thumbnail.save()
