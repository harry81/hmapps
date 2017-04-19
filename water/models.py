from django.db import models
from django.utils import timezone


class Item(models.Model):
    PUBLISHER_CHOICES = (
        ('h', 'hanis'),
        ('c', 'mk'),
    )
    url = models.CharField(max_length=256)
    publisher = models.CharField(max_length=1, choices=PUBLISHER_CHOICES)
    title = models.CharField(max_length=768, blank=True)
    subtitle = models.CharField(max_length=256, blank=True)
    text = models.TextField()
    row = models.TextField(blank=False)
    related_articles = models.ManyToManyField('self', blank=True)

    publish_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)
    created_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)
