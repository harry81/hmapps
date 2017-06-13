import django_filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Deal, Location
from .serializers import DealSerializer, LocationSerializer


class DealViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('location', )


class LocationViewSet(ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
