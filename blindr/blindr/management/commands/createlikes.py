import random
from typing import Any

import requests
from ...models import UserModel, DisplayModel, hobbiesModel
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="this will create random likes. You need to have the server running for this, \nas it uses the /setlikes url, so mutual likes are automatically handled"
    def handle(self, *args: Any, **options: Any) -> str | None:
        all_user_models = UserModel.objects.all()
        all_user_ids = [user.userId for user in all_user_models]
        for user in all_user_models:
            for _ in range(random.randint(0, all_user_ids.__len__())):
                response = requests.post("http://127.0.0.1:8000/tryMatch/", json={
                    "uid":str(user.userId),
                    "otherid":str(all_user_ids[random.randint(0, len(all_user_ids)-1)])
                })
            print(response.json())
                