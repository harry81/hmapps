from django.core.management.base import BaseCommand
import requests

class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        url = "http://www.hani.co.kr/arti/economy/economy_general/787918.html"
        rep = requests.get(url)
        print rep.ok
