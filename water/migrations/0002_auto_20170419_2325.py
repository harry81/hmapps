# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('water', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='item',
            name='related_articles',
        ),
        migrations.RemoveField(
            model_name='item',
            name='row',
        ),
    ]
