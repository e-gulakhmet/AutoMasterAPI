from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from main.pagination import StandardResultsSetPagination
from masters import serializers
from masters.filters import MasterFilterSet
from masters.models import Master


class MasterRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.all()


class MasterListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.annotate(Count('registers')).order_by('-registers__count')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MasterFilterSet
