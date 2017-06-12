from rest_framework import serializers
from .models import Deal, Location


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
