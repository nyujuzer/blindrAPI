from enum import Enum
from datetime import datetime
from moviepy.editor import VideoFileClip
from .settings import MEDIA_ROOT
from os import path, mkdir
from apscheduler.schedulers.background import BackgroundScheduler
# from .jobs import tasks_manager

class Globals:
        class EGender(Enum):
                MALE = 1
                FEMALE = 2
                ENBY = 3
                ANY = 4
                NONE = 404
        class Gender():
                def Encode(nem) -> int:
                        return Globals.EGender[nem].value
    
                def Decode(code) -> str:
                        return Globals.EGender(code).name


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
        def handleIdempotenceSetToken(idempotence):
                tokenElements = idempotence.split(";")
                print(tokenElements)
                initialTimeStamp = tokenElements[0].split("/")
                initialTimeStampList = [i.split("-") for i in initialTimeStamp]
                endTimeStamp = tokenElements[1].split("/")
                endTimeStampList = [i.split("-") for i in endTimeStamp]
                initialTime = datetime(year=int(initialTimeStampList[0][0]),
                                                month=int(initialTimeStampList[0][1]),
                                                day=int(initialTimeStampList[0][2]),
                                                hour=int(initialTimeStampList[1][0]),
                                                minute=int(initialTimeStampList[1][1]))
                endTime = datetime(year=int(endTimeStampList[0][0]),
                                                month=int(endTimeStampList[0][1]),
                                                day=int(endTimeStampList[0][2]),
                                                hour=int(endTimeStampList[1][0]),
                                                minute=int(endTimeStampList[1][1]))
                userDetails = tokenElements[2].split("/")
        def handleIdempotence(idempotence):
                pass