# -*- coding: utf-8 -*-
import json
import os
import requests
from django.core.management.base import BaseCommand
from earth.models import Address, AddressCode
from earth.utils import get_gugunlist, get_deal


url_get_gugunlist = "http://rt.molit.go.kr/srh/getGugunListAjax.do"

SI = [
    {"CODE": "11", "NAME": u"서울특별시"},
    {"CODE": "26", "NAME": u"부산광역시"},
    {"CODE": "27", "NAME": u"대구광역시"},
    {"CODE": "28", "NAME": u"인천광역시"},
    {"CODE": "29", "NAME": u"광주광역시"},
    {"CODE": "30", "NAME": u"대전광역시"},
    {"CODE": "31", "NAME": u"울산광역시"},
    {"CODE": "36", "NAME": u"세종특별자치시"},
    {"CODE": "41", "NAME": u"경기도"},
    {"CODE": "42", "NAME": u"강원도"},
    {"CODE": "43", "NAME": u"충청북도"},
    {"CODE": "44", "NAME": u"충청남도"},
    {"CODE": "45", "NAME": u"전라북도"},
    {"CODE": "46", "NAME": u"전라남도"},
    {"CODE": "47", "NAME": u"경상북도"},
    {"CODE": "48", "NAME": u"경상남도"},
    {"CODE": "50", "NAME": u"제주특별자치도"},
]


def process_deal(resp):
    for line in resp:
        for x in range(1, 4):
            monthlist = "month%sList" % x
            deals = line[monthlist]
            for deal in deals:
                print deal['BLDG_NM'], deal['SUM_AMT'], deal['BLDG_AREA'], deal['APTFNO'], deal['DEAL_MM']


# curl http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev\?LAWD_CD\=47190\&DEAL_YMD\=201701\&numOfRows\=1000\&serviceKey\=auRRfe7N35QzfgB8TuK41hLH%2Bsjwp8Vp7Q4ot8VaoRsnA0qsPHX65GonUcnkKfRzkBPdYz2h7llYNLRo19RJ2w%3D%3D | xmllint --format - > detail_47190_201701.xml


class Command(BaseCommand):
    def handle(self, *args, **options):

        address = {}

        addr = dict.fromkeys(['sidoCode', 'gugunCode', 'dongCode', 'danjiCode'])
        for si in SI:
            addr['sidoCode'] = si['CODE']
            guns = get_gugunlist(si)

            address[int(si['CODE'])] = {
                'guguns': guns,
                'name': si['NAME']
            }

        with open('/tmp/address.json', 'wt') as fp:
            fp.write(json.dumps(address, sort_keys=True))
