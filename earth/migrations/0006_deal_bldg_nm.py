# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0005_auto_20170530_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='bldg_nm',
            field=models.CharField(default='', max_length=32, verbose_name='\uc544\ud30c\ud2b8'),
            preserve_default=False,
        ),
    ]
