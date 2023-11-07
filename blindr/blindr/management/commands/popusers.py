import json
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker
import requests
from ...models import UserModel, DisplayModel, hobbiesModel
import random

class Command(BaseCommand):
    help = 'Populate users'
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number", type=int)    
    def handle(self, *args, **options):
                
        f = Faker()
        genders = ["MALE","FEMALE","ENBY", "ANY"]
        for _ in range(options['number']):
            password = f.password()
            print(f.date())
            response = requests.post("http://127.0.0.1:8000/register/",json=(
           {"email": f.email(),
                            "password": password,
                            "conf": password,
                            "name": f.name(),
                            "gender": genders[random.randint(0, 2)],
                            "preferences":genders[random.randint(0, 3)],
                            "hobbies": [random.randint(1, 12)],
                            "age": f.date(),
                            }
                )
            )
            
            print(response.json())