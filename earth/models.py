# -*- coding: utf-8 -*-

from django.db import models


class Address(models.Model):
    sido_code = models.CharField(max_length=32)
    gugun_code = models.CharField(max_length=32)
    dong_code = models.CharField(max_length=32, unique=True)


class AddressCode(models.Model):
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32, unique=True)
    gubun = models.CharField(max_length=32)


class Deal(models.Model):
    sum_amount = models.IntegerField(u'거래금액')
    bldg_yy = models.CharField(u'건축년도', max_length=32)
    dong = models.CharField(u'법정동', max_length=32)
    bldg_nm = models.CharField(u'아파트', max_length=32)
    deal_yy = models.CharField(u'년', max_length=32)
    deal_mm = models.CharField(u'월', max_length=32)
    deal_dd = models.CharField(u'일', max_length=32)
    bldg_area = models.CharField(u'전용면적', max_length=32)
    bobn = models.CharField(u'지번', max_length=32)
    area_cd = models.CharField(u'지역코드', max_length=32)
    aptfno = models.CharField(u'층', max_length=32)
