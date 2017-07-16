# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.cache import cache
from .utils import (get_content_with_key,
                    get_s3_keys,
                    convert_data_to_json,
                    update_deals,
                    create_deals,
                    _get_data_go_kr_key)
from earth.models import Deal, _address_to_geolocation


class ArticlesTestCase(TestCase):
    fixtures = ['deals']

    def setUp(self):
        pass


class DealsTeatCase(TestCase):

    def test_bulk_create(self):
        path = u'2016/04/47190_구미시.xml'

        content = get_content_with_key(path=path)
        data_json = convert_data_to_json(content)
        condition = {"origin": path}
        create_deals(data_json, origin=path)

        for deal in Deal.objects.filter(origin=path):
            print deal.update_location()

    def test_get_s3_keys(self):
        list_of_keys = get_s3_keys(u'2016/04')

    def test_update_deals(self):
        update_deals(year=2016, month='2')

    def test_update_deals_without_month(self):
        update_deals(year=2016)

    def test_address_to_geolocation(self):
        params = {'q': '대화동 2212'}
        item = _address_to_geolocation(**params)
        for k, v in item.items():
            print k, v

    def test_get_data_go_kr_key(self):
        data_key = cache.get('DATA_KEY')
        self.assertEqual(data_key, "DATA_GO_KR_KEY1")

        _get_data_go_kr_key()

        data_key = cache.get('DATA_KEY')
        self.assertEqual(data_key, "DATA_GO_KR_KEY2")
