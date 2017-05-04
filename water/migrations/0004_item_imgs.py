# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0003_auto_20170503_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='imgs',
            field=django.contrib.postgres.fields.ArrayField(null=True, base_field=models.CharField(max_length=256, blank=True), size=8),
        ),
    ]
