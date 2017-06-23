# -*- coding: utf-8 -*-
import os
from os import listdir
from os.path import isfile, join
import json
import xmltodict
import requests
import boto3
from botocore.exceptions import ClientError

from django.core.management.base import BaseCommand
from earth.utils import rename_fields, get_deal

s3 = boto3.client('s3')
bucket_name = 'hm-deals'


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
        parser.add_argument('--when')

    def handle(self, *args, **options):
        addresses = {}

        with open('/tmp/address.json', 'rt') as fp:
            addresses = json.loads(fp.read())

        year = '2016'
        params = {}

        for month in range(1, 13):
            when = "%s%02d" % (year, month)

            for si in addresses:
                for gun in addresses[si]['guguns']:
                    filename = "%s_%s.xml" % (gun['CODE'], gun['NAME'])
                    path = "%s/%02d/%s" % (year, month, filename)

                    try:
                        s3_obj = s3.get_object(Bucket=bucket_name, Key=path)
                        size_obj = s3_obj['ContentLength']
                        print "Already there [%10s] - %d" % (path, size_obj)

                    except ClientError as ex:
                        full_path = get_deal(when, gugunCode=gun['CODE'], filename=filename)
                        if ex.response['Error']['Code'] == 'NoSuchKey':
                            s3.upload_file(full_path, bucket_name, path)
                            print "Saved at S3 [%20s] - %d" % (path, os.stat(full_path).st_size)

                        else:
                            raise ex

        filename = '/tmp/address.json'
        s3.upload_file(filename, bucket_name, 'address.json')
