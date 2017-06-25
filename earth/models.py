# -*- coding: utf-8 -*-

import requests
from django.db import IntegrityError
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


client_id = "mAGsI5imdDqwwg8LwhJH"
client_secret = "58rX8bWARl"


class Address(models.Model):
    sido_code = models.CharField(max_length=32)
    gugun_code = models.CharField(max_length=32)
    dong_code = models.CharField(max_length=32, unique=True)


class AddressCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    gubun = models.CharField(max_length=32)


class Location(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    point = models.PointField(default='POINT (0 0)', srid=4326)
    isRoadAddress = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    sigugun = models.CharField(max_length=32, null=True, blank=True)
    dongmyun = models.CharField(max_length=32, null=True, blank=True)
    rest = models.CharField(max_length=32, null=True, blank=True)
    sido = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.dongmyun, self.sido, self.rest)

    def num_of_deals(self):
        return self.deals.count()


class Deal(models.Model):
    sum_amount = models.IntegerField(u'거래금액')
    bldg_yy = models.CharField(u'건축년도', max_length=32)
    dong = models.CharField(u'법정동', max_length=32)
    bldg_nm = models.CharField(u'아파트', max_length=256)
    deal_yy = models.CharField(u'년', max_length=32)
    deal_mm = models.CharField(u'월', max_length=32)
    deal_dd = models.CharField(u'일', max_length=32)
    bldg_area = models.CharField(u'전용면적', max_length=32)
    bobn = models.CharField(u'지번', max_length=32)
    area_cd = models.CharField(u'지역코드', max_length=32)
    aptfno = models.CharField(u'층', max_length=32)
    origin = models.CharField(u'추출경로', max_length=256, null=True, blank=True)
    location = models.ForeignKey(Location, related_name="deals", null=True, blank=True)

    class Meta:
        ordering = ['-deal_yy', '-deal_mm', '-deal_dd']

    def __unicode__(self):
        return "%s %s" % (self.bldg_nm, self.bldg_area)

    def _flatten_dict(self, item):
        addrdetail = item.pop('addrdetail', None)

        if addrdetail:
            for k, v in addrdetail.items():
                item[k] = v

        return item

    def save(self, *args, **kwargs):
        url = "https://openapi.naver.com/v1/map/geocode?query=%s %s" % (self.dong, self.bobn)

        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            item = self._flatten_dict(response.json()['result']['items'][0])
            point_dict = item.pop('point', None)
            point = Point(**point_dict)

            try:
                location, created = Location.objects.get_or_create(
                    point=point, name=self.bldg_nm, defaults={"point": point}, **item)

                self.location = location

            except IntegrityError as e:
                import ipdb; ipdb.set_trace()

        response = super(Deal, self).save(*args, **kwargs)
        return response

    def update_location(self):
        if self.location:
            return 'ok'

        url = "https://openapi.naver.com/v1/map/geocode?query=%s %s" % (self.dong, self.bobn)

        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            item = self._flatten_dict(response.json()['result']['items'][0])
            point_dict = item.pop('point', None)
            point = Point(**point_dict)

            try:
                location, created = Location.objects.get_or_create(
                    point=point, name=self.bldg_nm, defaults={"point": point}, **item)

                self.location = location
                self.save()

            except IntegrityError as e:
                import ipdb; ipdb.set_trace()

        return '%s %s updated' % (self.bldg_nm, self.location)
