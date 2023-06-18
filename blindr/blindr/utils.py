import requests

def get_geolocation(request):
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip:
        ip = user_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey=aa07d509d7e34d6e97147cf96bf28b06&ip={ip}'

    try:
        response = requests.get(url)
        data = response.json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        city = data.get('city')
        country = data.get('country_name')

        return latitude, longitude, city, country

    except requests.exceptions.RequestException as e:
        # Handle error cases
        print(f"Error: {e}")
        return None, None, None, None
from .models import UserModel, DisplayModel

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
    
