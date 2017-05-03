# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0002_auto_20170419_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='publisher',
            field=models.CharField(max_length=1, choices=[(b'h', b'hanis'), (b'm', b'mk')]),
        ),
    ]
