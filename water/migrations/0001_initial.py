# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('publisher', models.CharField(max_length=1, choices=[(b'h', b'hanis'), (b'c', b'mk')])),
                ('title', models.CharField(max_length=768, blank=True)),
                ('subtitle', models.CharField(max_length=256, blank=True)),
                ('text', models.TextField()),
                ('row', models.TextField()),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, db_index=True, blank=True)),
                ('related_articles', models.ManyToManyField(related_name='_item_related_articles_+', to='water.Item', blank=True)),
            ],
        ),
    ]
