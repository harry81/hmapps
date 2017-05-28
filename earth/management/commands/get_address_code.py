# -*- coding: utf-8 -*-
import json
import requests
from django.core.management.base import BaseCommand

url_get_gugunlist = "http://rt.molit.go.kr/srh/getGugunListAjax.do"

SI = {
    11: u"서울특별시",
    26: u"부산광역시",
    27: u"대구광역시",
    28: u"인천광역시",
    29: u"광주광역시",
    30: u"대전광역시",
    31: u"울산광역시",
    36: u"세종특별자치시",
    41: u"경기도",
    42: u"강원도",
    43: u"충청북도",
    44: u"충청남도",
    45: u"전라북도",
    46: u"전라남도",
    47: u"경상북도",
    48: u"경상남도",
    50: u"제주특별자치도",
}


# # 동 구하기
# curl 'http://rt.molit.go.kr/srh/getGugunListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'sidoCode=47'
# 구미 - 47190
def get_gugunlist(sidocode):
    response = requests.get("http://rt.molit.go.kr/srh/getGugunListAjax.do",
                            params={"sidoCode": sidocode})
    return response.content


# # 구군구하기
# curl 'http://rt.molit.go.kr/srh/getDongListAjax.do'  -H 'Origin: http://rt.molit.go.kr'   --data 'gugunCode=47830'
def get_donglist(guguncode):
    response = requests.get("http://rt.molit.go.kr/srh/getDongListAjax.do",
                            params={"gugunCode": guguncode})
    return response.content


# # 단지 구하기
# curl 'http://rt.molit.go.kr/srh/getDanjiComboAjax.do' --data 'menuGubun=A&houseType=1&srhYear=2017&srhPeriod=2&gubunCode=LAND&dongCode=1121510900'
def get_danjicombo(dongcode):
    response = requests.get("http://rt.molit.go.kr/srh/getDanjiComboAjax.do",
                            params={"dongCode": dongcode,
                                    "menuGubun": "A",
                                    "houseType": 1,
                                    "srhYear": 2017,
                                    "srhPeriod": 2,
                                    "gubunCode": "LAND"
                                })
    return response.content


def print_addr(addr):
    print addr['CODE'], addr['NAME']


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        for si in SI:
            guns = get_gugunlist(si)
            for gun in json.loads(guns)['jsonList']:
                dongs = get_donglist(gun['CODE'])
                for dong in json.loads(dongs)['jsonList']:
                    print_addr(dong)
                    danji = get_danjicombo(dong['CODE'])
                    print danji

