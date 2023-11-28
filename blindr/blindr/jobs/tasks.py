import datetime
from blindr.models import UserModel, DisplayModel, MatchesModel
from blindr.utils import isReciprocated

class counter():
   count = 0
def my_periodic_task():
   print(counter.count, datetime.datetime.now().second)
   counter.count += 1


def handleEphemerals():
   delEphemerals()
   makeEphemerals()

def delEphemerals():
   n = 0
   all_matches = MatchesModel.objects.all()
   _match:MatchesModel
   for _match in all_matches:
      if _match.ephemeral:
         _match.delete()
         n+=1
   print(f'deleted {n} matches')
         


def makeEphemerals():
   """
   
   """
   all_users = UserModel.objects.all()
   user:UserModel
   like:DisplayModel
   for user in all_users:
      likes = user.currentLikes.all()
      for like in likes:
         if not isReciprocated(user, like):
             MatchesModel.objects.create(user_1 = user, user_2=like.account, ephemeral=True )
             break
   print("made ephemeral matches")