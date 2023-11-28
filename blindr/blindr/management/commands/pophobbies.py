import json
from django.core.management.base import BaseCommand
from ...models import hobbiesModel


class Command(BaseCommand):
    help = 'Populate hobbies in the Django server'

    def handle(self, *args, **options):
        with open('hobbies.json') as f:
            data = json.load(f)
            hobbies = data['hobbies']
            for hobby_data in hobbies:
                hobby_id = hobby_data['id']
                hobby_name = hobby_data['hobby']
                hobbiesModel.objects.get_or_create(id=hobby_id, hobby=hobby_name)
