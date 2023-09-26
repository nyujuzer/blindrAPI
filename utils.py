import math
from .models import UserModel
def calculate_distance(lat1, lon1, lat2, lon2):
     # Calculate the difference in x and y coordinates
    x_diff = lat1 - lat2
    y_diff = lon1 - lon2
    
    # Calculate the square of the differences
    x_diff_squared = x_diff ** 2
    y_diff_squared = y_diff ** 2
    
    # Sum the squared differences and take the square root to get the distance
    distance = math.sqrt(x_diff_squared + y_diff_squared)
    return distance
def EmailIsAvailable(_email):
    '''
    _email:str -- the email of the user. 

    returns: false if objects.all() has a length more than 0, and true if its 0 
    '''
    length = len(UserModel.objects.all().filter(email=_email))
    print(length)
    if length == 0:
        return True
    else:
        return False
    
class stream():
    def __init__(self) -> None:
        self.requests = []
    def acc_subscriber(self, request):
        self.requests.append(request)
    