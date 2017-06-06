from django.test import TestCase
from earth.models import Deal


class ArticlesTestCase(TestCase):
    fixtures = ['deals']

    def setUp(self):
        pass

    def test_start(self):
        deal = Deal.objects.first()
        deal.get_lnglat()
