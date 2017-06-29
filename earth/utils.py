# -*- coding: utf-8 -*-
import os
import re
import locale
import xmltodict
import requests
import boto3
from botocore.client import Config
from django.conf import settings


from .models import Deal

s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                  config=Config(signature_version='s3v4'))

bucket_name = 'hm-deals'


def get_s3_keys(prefix=''):
    """
    bucket내에서 prefix에 해당하는 파일이름만 리스트로 돌려준다.
    """
    keys = []

    paginator = s3.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

    for page in page_iterator:
        for ele in page['Contents']:
            keys.append(ele['Key'])

    return keys


def get_content_with_key(path='2016/04/47770_영덕군.xml'):
    """
    해당 키에 해당하는 파일의 내용을 돌려준다.
    """
    s3_obj = s3.get_object(Bucket=bucket_name, Key=path)
    body = s3_obj['Body']
    content = body.read()
    return content


def convert_data_to_json(content):
    """
    input - content : xml 형식의 파일 내용
    output - 필드명이 변경된 json 형식
    """
    deals = xmltodict.parse(content)
    renamed_items = []

    if int(deals['response']['body']['totalCount']) == 0:
        return renamed_items

    try:
        items = deals['response']['body']['items']['item']
    except TypeError as e:
        print "Exception %s - %s" % (e, content)
        return None

    if not isinstance(items, list):
        items = [items, ]

    for item in items:
        try:
            renamed_items.append(rename_fields(item))
        except KeyError as e:
            print "%s %s" % (e, content)
            continue

    return renamed_items


def create_deals(data_json, origin):
    print "Create deals on %s" % origin

    deals = []

    for ele in data_json:
        ele['origin'] = origin
        ele['area_nm'] = re.sub(r"[\x00-\x7f]+", "", origin).encode('utf8')
        deals.append(Deal(**ele))

    try:
        Deal.objects.bulk_create(deals)
        print "%s %d created" % (origin, len(deals))
    except Exception as e:
        print "Exception %s at create_deals" % e

    return origin


def delete_deals(condition):
    Deal.objects.filter(**condition).delete()


def update_deals(year='2016', month=None):

    if year:
        _year = year[0]

    if month:
        _month = month[0]

    prefix = u'%s' % _year

    if not month:
        print "Month shouldn't be None"
        return

    prefix = u"%s/%02d" % (prefix, int(_month))
    list_of_keys = get_s3_keys(prefix)

    for key_name in list_of_keys:
        content = get_content_with_key(key_name)
        try:
            data_json = convert_data_to_json(content)
        except Exception as e:
            print "Exception %s at update_deals %s" % (e, key_name)
            continue

        if not data_json:
            continue

        condition = {"origin": key_name}
        delete_deals(condition)
        create_deals(data_json, origin=key_name)

        for deal in Deal.objects.filter(origin=key_name):
            try:
                print deal.update_location()

            except KeyError as e:
                print "%s" % e
                return

    return list_of_keys


def rename_fields(item):
    ret = {}

    try:
        ret['sum_amount'] = locale.atoi(item[u'거래금액'].replace(',', ''))
    except Exception as e:
        import ipdb; ipdb.set_trace()
        print "Exception %s at sum_amount of rename_fields" % e

    ret['bldg_yy'] = item[u'건축년도'].encode('utf-8')
    ret['bldg_nm'] = item[u'아파트'].encode('utf-8')
    ret['dong'] = item[u'법정동'].encode('utf-8')
    ret['deal_yy'] = item[u'년'].encode('utf-8')
    ret['deal_mm'] = item[u'월'].encode('utf-8')
    ret['deal_dd'] = item[u'일'].encode('utf-8')
    ret['bldg_area'] = item[u'전용면적'].encode('utf-8')

    if u'지번' in item:
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
