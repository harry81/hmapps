# -*- coding: utf-8 -*-
import os
import json
import xmltodict
import requests
import boto3
from botocore.exceptions import ClientError

from django.core.management.base import BaseCommand
from earth.utils import rename_fields, get_deal, convert_data_to_json


class NeedMoreItems(Exception):
    """ Easy to understand naming conventions work best! """
    pass


s3 = boto3.client('s3')
bucket_name = 'hm-deals'

EXCEED_LIMIT = "LIMITED NUMBER OF SERVICE REQUESTS EXCEEDS ERROR."


def import_deals(url, origin):
    deals_as_string = open(origin, 'r').read()
    deals = xmltodict.parse(deals_as_string)

    if len(deals_as_string) < 2048:
        return

    cnt = 0
    items = deals['response']['body']['items']['item']
    for item in items:
        try:
            item = rename_fields(item)
        except KeyError as e:
            print e
            continue

        item['origin'] = origin
        res = requests.post("%s/en/api/earth/deal/" % url, data=item)
        cnt += 1
        print "[%4d:%4d]" % (cnt, len(items)), "{bldg_nm} {area_cd} {bobn} {sum_amount} {dong}".format(**item), res


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='+')
        parser.add_argument('--year', type=int)
        parser.add_argument('--month', type=int)

    def handle(self, *args, **options):
        addresses = {}

        with open('address.json', 'rt') as fp:
            addresses = json.loads(fp.read())

        month = options.get('month', 1)
        year = options.get('year', 2016)

        for month in range(month, 13):
            when = "%d%02d" % (year, month)

            for si in addresses:
                for gun in addresses[si]['guguns']:
                    filename = "%s_%s.xml" % (gun['CODE'], gun['NAME'])
                    path = "%s/%02d/%s" % (year, month, filename)

                    try:
                        s3_obj = s3.get_object(Bucket=bucket_name, Key=path)
                        size_obj = s3_obj['ContentLength']

                        body = s3_obj['Body']
                        raw_body = xmltodict.parse(body.read())
                        total_count = raw_body['response']['body']['totalCount']
                        num_of_rows = raw_body['response']['body']['numOfRows']

                        if num_of_rows > total_count:
                            """ s3에 저장된 deal에 더 받아야할 데이타가 있다면, 파일을 삭제한 후 다시 s3 객체를 get한다.
                            의도적으로 예외를 발생하여 해당 객체를 다시 다운로드할수 있게 한다.

                            """
                            s3.delete_object(Bucket=bucket_name, Key=path)
                            s3.get_object(Bucket=bucket_name, Key=path)

                        print "Already there [%10s] - %d" % (path, size_obj)

                        if size_obj < 250:
                            content = s3_obj['Body']

                            if EXCEED_LIMIT in content.read():
                                s3.delete_object(Bucket=bucket_name, Key=path)
                                print "[%30s] %s is deleted." % (EXCEED_LIMIT, path)

                    except ClientError as ex:
                        if ex.response['Error']['Code'] == 'NoSuchKey':
                            full_path = get_deal(when, gugunCode=gun['CODE'], filename=filename)

                            with open(full_path, 'rt') as fp:
                                if EXCEED_LIMIT in fp.read():
                                    print "[%s] %s" % (EXCEED_LIMIT, path)
                                    return

                            s3.upload_file(full_path, bucket_name, path)
                            print "Saved at S3 [%10s] - %d" % (path, os.stat(full_path).st_size)

                        else:
                            raise ex
