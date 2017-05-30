# -*- coding: utf-8 -*-
import requests
import locale
import xmltodict
from django.core.management.base import BaseCommand
from earth.models import Deal


def rename_fields(item):
    ret = {}

    ret['sum_amount'] = locale.atoi(item[u'거래금액'].replace(',',''))
    ret['bldg_yy'] = item[u'건축년도']
    ret['bldg_nm'] = item[u'아파트']
    ret['dong'] = item[u'법정동']
    ret['deal_yy'] = item[u'년']
    ret['deal_mm'] = item[u'월']
    ret['deal_dd'] = item[u'일']
    ret['bldg_area'] = item[u'전용면적']
    ret['bobn'] = item[u'지번']
    ret['area_cd'] = item[u'지역코드']
    ret['aptfno'] = item[u'층']

    deal = Deal.objects.create(**ret)
    return deal


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        deals_as_string = open('list_47190_201701.xml', 'r').read()
        deals = xmltodict.parse(deals_as_string)

        for item in deals['response']['body']['items']['item']:
            item = rename_fields(item)
            print item
