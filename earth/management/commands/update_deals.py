# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from earth.utils import update_deals


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--url', nargs='+')
        parser.add_argument('--year', type=int)
        parser.add_argument('--month', type=int)

    def handle(self, *args, **options):
        update_deals(**options)
