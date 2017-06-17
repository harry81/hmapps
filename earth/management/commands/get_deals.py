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

        if len(deals_as_string) < 2048:
                return

        cnt = 1
        items = deals['response']['body']['items']['item']
        for item in items:
            try:
                item = rename_fields(item)
            except KeyError as e:
                print e
                continue

            item['origin'] = origin
            res = requests.post("%s/en/api/earth/deal/" % url, data=item)
            print "[%4d:%4d]" % (cnt, len(items)), "{origin}-{bldg_nm} {area_cd} {bobn} {sum_amount} {dong}".format(**item), res


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='+')
        parser.add_argument('--when')

    def handle(self, *args, **options):
        url = 'http://localhost:8001'

        if options['url']:
            url = options['url'][0]

        if options['when']:
            when = options['when']

        list_path = 'list/%s' % when

        onlyfiles = [f for f in listdir(list_path) if isfile(join(list_path, f))]

        for dest in onlyfiles:
            filename = "%s/%s" % (list_path, dest)
            import_deals(url, filename)
