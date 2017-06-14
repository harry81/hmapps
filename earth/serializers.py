from rest_framework import serializers
from .models import Deal, Location


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal


class LocationSerializer(serializers.ModelSerializer):
    deals = DealSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super(LocationSerializer, self).__init__(*args, **kwargs)

        excludes = []

        if 'context' not in kwargs:
            return

        elif kwargs['context']['view'].action == 'list':
            excludes = ['deals']

            for exclude in excludes:
                self.fields.pop(exclude)

    class Meta:
        model = Location
