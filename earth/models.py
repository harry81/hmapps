# -*- coding: utf-8 -*-

import time
import requests
from django.db import IntegrityError
from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.gis.geos import Point
from model_utils.models import TimeStampedModel


def _address_to_geolocation(**kwargs):
    url_add2coord = "https://apis.daum.net/local/v1/geo/addr2coord"

    params = {}
    params['apikey'] = settings.DAUM_API_KEY
    params['output'] = 'json'

    params.update(kwargs)

    cnt = 3

    while(cnt > 0):
        try:
            cnt -= 1
            response = requests.get(url_add2coord, params=params)
            break

        except Exception as e:
            if cnt < 0:
                print (e)
                import ipdb; ipdb.set_trace()
            else:
                print ("wait and again %d" % cnt)
                time.sleep(3 - cnt)
                continue

    try:
        item = response.json()['channel']['item'][0]
    except IndexError as e:
        print ("%s : %s" % (e, params['q']))
        return None

    except KeyError as e:
        raise KeyError(response.json())

    return item


def _amend_location(response):
    location = response.copy()
    unused_fields = ['point_wx', 'point_wy', 'point_x', 'point_y']

    for field in unused_fields:
        location.pop(field, None)

    lat = location.pop('lat', None)
    lng = location.pop('lng', None)

    point = Point(lng, lat)
    location['point'] = point

    location['daum_geo_id'] = location.pop('id', None)

    return location


class Address(TimeStampedModel):
    sido_code = models.CharField(max_length=32)
    gugun_code = models.CharField(max_length=32)
    dong_code = models.CharField(max_length=32, unique=True)


class AddressCode(TimeStampedModel):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    gubun = models.CharField(max_length=32)


class Location(TimeStampedModel):
    bldg_nm = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    mountain = models.CharField(max_length=32, null=True, blank=True)
    mainAddress = models.CharField(max_length=32, null=True, blank=True)
    point = models.PointField(default='POINT (0 0)', srid=4326)
    localName_1 = models.CharField(max_length=32, null=True, blank=True)
    localName_2 = models.CharField(max_length=32, null=True, blank=True)
    localName_3 = models.CharField(max_length=32, null=True, blank=True)

    isNewAddress = models.CharField(max_length=2, null=True, blank=True)
    buildingAddress = models.CharField(max_length=64, null=True, blank=True)
    placeName = models.CharField(max_length=32, null=True, blank=True)
    zipcode = models.CharField(max_length=32, null=True, blank=True)
    newAddress = models.CharField(max_length=256, null=True, blank=True)
    zone_no = models.CharField(max_length=32, null=True, blank=True)
    subAddress = models.CharField(max_length=32, null=True, blank=True)

    daum_geo_id = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.title)

    def num_of_deals(self):
        return self.deals.count()


class Deal(TimeStampedModel):
    sum_amount = models.IntegerField(u'거래금액')
    bldg_yy = models.CharField(u'건축년도', max_length=32)
    dong = models.CharField(u'법정동', max_length=32)
    bldg_nm = models.CharField(u'아파트', max_length=256)
    deal_yy = models.IntegerField(u'년', db_index=True)
    deal_mm = models.IntegerField(u'월', db_index=True)
    deal_dd = models.CharField(u'일', max_length=32, db_index=True)
    bldg_area = models.FloatField(u'전용면적', max_length=32)
    bobn = models.CharField(u'지번', max_length=32)
    area_cd = models.CharField(u'지역코드', max_length=32)
    area_nm = models.CharField(u'지역이름', max_length=32, default='')
    aptfno = models.CharField(u'층', max_length=32)
    origin = models.CharField(u'추출경로', max_length=256, null=True, blank=True)
    location = models.ForeignKey(Location, related_name="deals", null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.bldg_nm, self.bldg_area)

    def _flatten_dict(self, item):
        addrdetail = item.pop('addrdetail', None)

        if addrdetail:
            for k, v in addrdetail.items():
                item[k] = v

        return item

    def save(self, *args, **kwargs):
        response = super(Deal, self).save(*args, **kwargs)
        return response

    def update_location(self):
        """
        0 it has the location
        1 updated with existing location
        2 create new location and update with it

        """
        if self.location:
            return 'Location is already there %s[%d] %s' % (self.bldg_nm, self.pk, self.location)

        loc = Location.objects.filter(title__contains="%s %s %s" % (self.area_nm, self.dong, self.bobn))

        if loc.exists():
            self.location = loc[0]
            self.save()

            return 'Location updated with the existing one %s[%d] %s' % (self.bldg_nm, self.pk, self.location)

        params = {'q': "%s %s %s" % (self.area_nm, self.dong, self.bobn)}
        response = _address_to_geolocation(**params)

        if response:
            try:
                item = _amend_location(response)
            except IndexError as e:
                print (e)
                import ipdb; ipdb.set_trace()

            point = item.pop('point', None)

            try:
                location, created = Location.objects.get_or_create(
                    point=point, bldg_nm=self.bldg_nm, defaults={"point": point}, **item)

                self.location = location
                self.save()

            except (IntegrityError, MultipleObjectsReturned) as e:
                import ipdb; ipdb.set_trace()

        return 'Location updated with new one %s[%d]' % (self.bldg_nm, self.pk)
