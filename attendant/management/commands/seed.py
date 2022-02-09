import requests
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'http://127.0.0.1:8000/api/auth/login/'
        url2 = 'http://127.0.0.1:8000/attendantapi/'
        user_and_pass = {'username': 'admin', 'password': 'amir1372'}
        response = requests.post(url, data=user_and_pass)
        print(response.json())





