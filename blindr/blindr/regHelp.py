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