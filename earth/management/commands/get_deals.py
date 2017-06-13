# -*- coding: utf-8 -*-
import xmltodict
import requests
from django.core.management.base import BaseCommand
from earth.utils import rename_fields


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='+')

    def handle(self, *args, **options):
        url = 'http://localhost:8001'

        if options['url']:
            url = options['url'][0]

        deals_as_string = open('list_47190_201701.xml', 'r').read()
        deals = xmltodict.parse(deals_as_string)

        for item in deals['response']['body']['items']['item']:
            item = rename_fields(item)
            res = requests.post("%s/en/api/earth/deal/" % url, data=item)
            print item, res
