from django.core.management.base import BaseCommand
from water.tasks import fetch_articles


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        # parser.add_argument('sample', nargs='+')
        parser.add_argument('--url', nargs='+')

    def handle(self, *args, **options):
        kwargs = {}
        for url in options['url']:
            kwargs['url'] = url

            url = kwargs.get('url', None)
            fetch_articles(**kwargs)
