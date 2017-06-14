# -*- coding: utf-8 -*-
import xmltodict
import requests
from django.core.management.base import BaseCommand
from earth.utils import rename_fields
from os import listdir
from os.path import isfile, join


def import_deals(url, origin):
        deals_as_string = open(origin, 'r').read()
        deals = xmltodict.parse(deals_as_string)

        for item in deals['response']['body']['items']['item']:
            try:
                item = rename_fields(item)
            except KeyError as e:
                print e
                continue

            item['origin'] = origin
            res = requests.post("%s/en/api/earth/deal/" % url, data=item)
            print "{origin}-{bldg_nm} {area_cd} {bobn} {sum_amount} {dong}".format(**item), res


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='+')

    def handle(self, *args, **options):
        url = 'http://localhost:8001'

        if options['url']:
            url = options['url'][0]

        list_path = 'list'

        onlyfiles = [f for f in listdir(list_path) if isfile(join(list_path, f))]

        for dest in onlyfiles:
            filename = "%s/%s" % (list_path, dest)
            import_deals(url, filename)
