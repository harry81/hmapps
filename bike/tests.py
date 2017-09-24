from rest_framework.test import APITestCase
from .models import StateCenter, Center
from .utils import camel_to_snake_as_dict


class BikeTeatCase(APITestCase):

    def setUp(self):
        self.item = {'stationLatitude': '37.612484', 'rackTotCnt': '10',
                     'stationId': 'ST-481', 'parkingBikeTotCnt': '10',
                     'stationName': '933. LG\uc11c\ube44\uc2a4 \uc5ed\ucd0c\uc810',
                     'stationLongitude': '126.914879'}

    def test_create_bikecenter(self):
        item = camel_to_snake_as_dict(self.item)
        StateCenter.objects.create(**item)

        self.assertTrue(StateCenter.objects.count() > 0)
        self.assertTrue(Center.objects.count() > 0)
