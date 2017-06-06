# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0006_deal_bldg_nm'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT (0 0)', srid=4326),
        ),
    ]
