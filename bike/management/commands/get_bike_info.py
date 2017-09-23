from django.core.management.base import BaseCommand
from bike.utils import load_bike_info_to_dynamo


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_bike_info_to_dynamo()
