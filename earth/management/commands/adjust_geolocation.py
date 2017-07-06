# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from earth.models import Location
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class Command(BaseCommand):
    """
    주소의 실제 위경도를 얻는 과정에서 발생한 문제를 개선한다.
    - 이전에 주소값을 이용해 실제의 위경도를 얻는 과정이 있었다.
    - 위경도와 얻어진 x, y값의 순서를 잘못 이해해서 위경도가 바뀌어진채로 저장이 되었다.

    """
    def add_arguments(self, parser):
        parser.add_argument('--num', type=int)

    def handle(self, *args, **options):
        num = options.get('num', 100)

        lat = 36
        lng = 128
        radius = 500
        point = Point(lng, lat)

        # print Location.objects.exclude(point__distance_lt=(point, Distance(km=radius))).count()

        locs = Location.objects.using('live').exclude(point__distance_lt=(point, Distance(km=radius)))
        print "before total %s" % locs.count()

        for loc in locs[:num]:
            print loc.id,
            if loc.point.x < 39:
                loc.point = Point(loc.point.y, loc.point.x)
                loc.save()

        locs = Location.objects.using('live').exclude(point__distance_lt=(point, Distance(km=radius)))
        print "\nafter total %s" % locs.count()
