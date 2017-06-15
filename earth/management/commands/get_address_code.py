# -*- coding: utf-8 -*-
import json
import os
import requests
from django.core.management.base import BaseCommand
from earth.models import Address, AddressCode

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


# # 동 구하기
# curl 'http://rt.molit.go.kr/srh/getGugunListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'sidoCode=47'
# 구미 - 47190
def get_gugunlist(sido):
    sidocode = sido['CODE']
    response = requests.get("http://rt.molit.go.kr/srh/getGugunListAjax.do",
                            params={"sidoCode": sidocode})
    return response.json()['jsonList']


# # 구군구하기
# curl 'http://rt.molit.go.kr/srh/getDongListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'gugunCode=47830'
def get_donglist(dong):
    guguncode = dong['CODE']
    response = requests.get("http://rt.molit.go.kr/srh/getDongListAjax.do",
                            params={"gugunCode": guguncode})
    return response.json()['jsonList']


# # 단지 구하기
# curl 'http://rt.molit.go.kr/srh/getDanjiComboAjax.do' --data 'menuGubun=A&houseType=1&srhYear=2017&srhPeriod=2&gubunCode=LAND&dongCode=1121510900'
def get_danjicombo(**addr):
    params = {
        "dongCode": None,
        "menuGubun": "A",
        "houseType": 1,
        "srhYear": 2017,
        "srhPeriod": 2,
        "gubunCode": "LAND"
    }
    params.update(addr)

    response = requests.get("http://rt.molit.go.kr/srh/getDanjiComboAjax.do",
                            params=params)
    return response.json()['jsonList']

#  curl 'http://rt.molit.go.kr/srh/getListAjax.do'
# -H 'Referer: http://rt.molit.go.kr/srh/srh.do?menuGubun=A&srhType=LOC&houseType=1&gubunCode=LAND'
# --data 'reqPage=SRH&menuGubun=A&srhType=LOC&houseType=1&srhYear=2017&srhPeriod=2&gubunCode=LAND&sidoCode=47&gugunCode=47190&dongCode=4719012800&danjiCode=20106373&rentAmtType=3' 
def get_list(**addr):
    headers = {
        "Referer": "http://rt.molit.go.kr/srh/srh.do?menuGubun=A&srhType=LOC&houseType=1&gubunCode=LAND"
    }
    
    params={
        "reqPage": "SRH",
        "menuGubun": "A",
        "srhType": "LOC",
        "houseType": "1",
        "srhYear": "2017",
        "srhPeriod": "2",
        "gubunCode": "LAND",
        "sidoCode": "47",
        "gugunCode": "47190",
        "dongCode": "4719012800",
        "danjiCode": "20106373",
        "rentAmtType": "3",
    }
    
    params.update(addr)
    response = requests.get("http://rt.molit.go.kr/srh/getListAjax.do",
                            headers=headers,
                            params=params
    )
    return response.json()['jsonList']


def process_deal(resp):
    for line in resp:
        for x in range(1, 4):
            monthlist = "month%sList" % x
            deals = line[monthlist]
            for deal in deals:
                print deal['BLDG_NM'], deal['SUM_AMT'], deal['BLDG_AREA'], deal['APTFNO'], deal['DEAL_MM']


# curl http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev\?LAWD_CD\=47190\&DEAL_YMD\=201701\&numOfRows\=1000\&serviceKey\=auRRfe7N35QzfgB8TuK41hLH%2Bsjwp8Vp7Q4ot8VaoRsnA0qsPHX65GonUcnkKfRzkBPdYz2h7llYNLRo19RJ2w%3D%3D | xmllint --format - > detail_47190_201701.xml

def get_deal(year=2017, gugunCode=10117, name=None):
    try:
        os.mkdir('list/%s' % year)
    except OSError:
        pass
        
    filename = "%s.xml" % name
    full_path = "list/%s/%s" % (year, filename)
    if os.path.isfile(full_path):
        if os.path.getsize(full_path) > 300:
            print "Already exists %s" % filename
            return

    url_get_deals = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"

    params = {
        "LAWD_CD": gugunCode,
        "DEAL_YMD": year,
        "numOfRows": 1000,
        "serviceKey": "auRRfe7N35QzfgB8TuK41hLH+sjwp8Vp7Q4ot8VaoRsnA0qsPHX65GonUcnkKfRzkBPdYz2h7llYNLRo19RJ2w=="
    }
    response = requests.get(url_get_deals, params=params)
    with open(full_path, 'wt') as fp:
        fp.write(response.content)
    
    return filename


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--when'
        )

    def handle(self, *args, **options):
        if not options['when']:
            return None

        year = options['when']
        addr = dict.fromkeys(['sidoCode', 'gugunCode', 'dongCode', 'danjiCode'])
        # SI = [
        #     {"CODE": "11", "NAME": u"서울특별시"},
        # ]

        for si in SI:
            addr['sidoCode'] = si['CODE']
            guns = get_gugunlist(si)
            for gun in guns:
                addr['gugunCode'] = gun['CODE']
                name = "list_%s_%s_%s_%s" % (year, addr["gugunCode"], si['NAME'], gun['NAME'])
                res = get_deal(year=year, gugunCode=addr['gugunCode'], name=name)
                print res
