from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .models import Deal
from .serializers import DealSerializer


class DealViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):

    queryset = Deal.objects.all()
    serializer_class = DealSerializer
