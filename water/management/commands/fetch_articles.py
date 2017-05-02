from django.core.management.base import BaseCommand
from water.utils import (fetch_news_to_S3,
                         load_from_S3,
                         insert_news_to_db)


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

        fetch_news_to_S3(url=url)
        articles = load_from_S3(url=url)
        import ipdb; ipdb.set_trace()
        # insert_news_to_db(articles)
