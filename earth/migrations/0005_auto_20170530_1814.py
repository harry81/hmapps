# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earth', '0004_deals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sum_amount', models.IntegerField(verbose_name='\uac70\ub798\uae08\uc561')),
                ('bldg_yy', models.CharField(max_length=32, verbose_name='\uac74\ucd95\ub144\ub3c4')),
                ('dong', models.CharField(max_length=32, verbose_name='\ubc95\uc815\ub3d9')),
                ('deal_yy', models.CharField(max_length=32, verbose_name='\ub144')),
                ('deal_mm', models.CharField(max_length=32, verbose_name='\uc6d4')),
                ('deal_dd', models.CharField(max_length=32, verbose_name='\uc77c')),
                ('bldg_area', models.CharField(max_length=32, verbose_name='\uc804\uc6a9\uba74\uc801')),
                ('bobn', models.CharField(max_length=32, verbose_name='\uc9c0\ubc88')),
                ('area_cd', models.CharField(max_length=32, verbose_name='\uc9c0\uc5ed\ucf54\ub4dc')),
                ('aptfno', models.CharField(max_length=32, verbose_name='\uce35')),
            ],
        ),
        migrations.DeleteModel(
            name='Deals',
        ),
    ]
