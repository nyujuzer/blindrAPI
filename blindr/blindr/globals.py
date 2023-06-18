from enum import Enum
from datetime import datetime

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
