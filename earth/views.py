import django_filters
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_gis.filters import DistanceToPointFilter
from .models import Deal, Location
from .serializers import DealSerializer, LocationSerializer
from .tasks import celery_load_deals


class DealViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('location', )

    @list_route(methods=['post'])
    def load_deals(self, request):
        celery_load_deals.apply_async(countdown=1, kwargs=request.data)
        return Response('ok')


class LocationViewSet(ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    distance_filter_field = 'point'
    filter_backends = (DistanceToPointFilter, )
    distance_filter_convert_meters = True
