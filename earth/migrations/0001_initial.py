# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sido_code', models.CharField(max_length=32)),
                ('gugun_code', models.CharField(max_length=32)),
                ('dong_code', models.CharField(max_length=32)),
                ('danji_code', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='AddressCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('gubun', models.CharField(max_length=32)),
            ],
        ),
    ]
