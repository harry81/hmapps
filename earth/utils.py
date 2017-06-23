# -*- coding: utf-8 -*-
import os
import locale
import requests


def flatten_dict(item):
    addrdetail = item.pop('addrdetail', None)

    if addrdetail:
        for k, v in addrdetail.items():
            item[k] = v

    return item


def rename_fields(item):
    ret = {}

    ret['sum_amount'] = locale.atoi(item[u'거래금액'].replace(',', ''))
    ret['bldg_yy'] = item[u'건축년도'].encode('utf-8')
    ret['bldg_nm'] = item[u'아파트'].encode('utf-8')
    ret['dong'] = item[u'법정동'].encode('utf-8')
    ret['deal_yy'] = item[u'년'].encode('utf-8')
    ret['deal_mm'] = item[u'월'].encode('utf-8')
    ret['deal_dd'] = item[u'일'].encode('utf-8')
    ret['bldg_area'] = item[u'전용면적'].encode('utf-8')
    ret['bobn'] = item[u'지번'].encode('utf-8')
    ret['area_cd'] = item[u'지역코드'].encode('utf-8')
    ret['aptfno'] = item[u'층'].encode('utf-8')

    return ret


def get_deal(year=2017, gugunCode=10117, filename=None):
    try:
        os.mkdir('list/%s' % year)
    except OSError:
        pass

    full_path = "list/%s/%s" % (year, filename)

    if os.path.isfile(full_path):
        if os.path.getsize(full_path) > 300:
            print "Already exists %s" % filename
            return full_path

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

    return full_path


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

 # curl 'http://rt.molit.go.kr/srh/getListAjax.do' \
 #     -H 'Referer: http://rt.molit.go.kr/srh/srh.do?menuGubun=A&srhType=LOC&houseType=1&gubunCode=LAND'\
 #     --data 'reqPage=SRH&menuGubun=A&srhType=LOC&houseType=1&srhYear=2017&srhPeriod=2&gubunCode=LAND&sidoCode=47&gugunCode=47190&dongCode=4719012800&danjiCode=20106373&rentAmtType=3'
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
