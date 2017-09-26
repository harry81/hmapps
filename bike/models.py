from django.contrib.gis.db import models
from model_utils.models import TimeStampedModel
from django.contrib.gis.geos import Point


class Center(TimeStampedModel):
    station_id = models.CharField(max_length=32, unique=True)
    point = models.PointField(default='POINT (0 0)', srid=4326)
    station_name = models.CharField('대여소 이름', max_length=128, null=True, blank=True)

    def __str__(self):
        return "%s" % self.station_id


class StateCenter(TimeStampedModel):
    center = models.ForeignKey(Center, related_name="state", null=True, blank=True)
    parking_bike_tot_cnt = models.IntegerField('현재 주차 수', db_index=True)
    rack_tot_cnt = models.IntegerField('총 주차 가능수', db_index=True)

    def __init__(self, *args, **kwargs):

        station_id = kwargs.pop('station_id', None)

        if station_id:
            lat = float(kwargs.pop('station_latitude', None))
            lng = float(kwargs.pop('station_longitude', None))

            center = dict(
                station_id=station_id,
                station_name=kwargs.pop('station_name', None),
                point=Point(lng, lat)
            )
            center, _ = Center.objects.get_or_create(
                station_id=center['station_id'], defaults=center)

            if center:
                kwargs['center'] = center

        super(StateCenter, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return "%s" % self.center
