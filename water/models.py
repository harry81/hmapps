from django.db import models
from django.utils import timezone


class Item(models.Model):
    PUBLISHER_CHOICES = (
        ('h', 'hanis'),
        ('m', 'mk'),
    )
    url = models.CharField(max_length=256)
    publisher = models.CharField(max_length=1, choices=PUBLISHER_CHOICES)
    title = models.CharField(max_length=768, blank=True)
    subtitle = models.CharField(max_length=256, blank=True)
    text = models.TextField()

    publish_at = models.DateTimeField(db_index=True,
                                      default=timezone.now, blank=True)

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):

        if isinstance(self.publish_at, list):
            self.publish_at = self.publish_at[0]

        super(Item, self).save(*args, **kwargs)
