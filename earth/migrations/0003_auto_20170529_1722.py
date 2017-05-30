# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0002_remove_address_danji_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='dong_code',
            field=models.CharField(unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='addresscode',
            name='code',
            field=models.CharField(unique=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='addresscode',
            name='name',
            field=models.CharField(unique=True, max_length=32),
        ),
    ]
