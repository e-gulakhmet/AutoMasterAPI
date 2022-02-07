from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from main.pagination import StandardResultsSetPagination
from masters import serializers
from masters.filters import MasterFilterSet
from masters.models import Master


free_at = openapi.Parameter('free_at', openapi.IN_QUERY, type=openapi.FORMAT_DATETIME,
                            description='Фильтрует мастеров, у которых нет записей на указанное время')


class MasterRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.all()


class MasterListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.annotate(Count('registers')).order_by('-registers__count')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MasterFilterSet

    @swagger_auto_schema(manual_parameters=[free_at])
    def get(self, request, *args, **kwargs):
        """
        Выводит всех мастеров.
        Выше тот, у кого больше записей.
        """
        return super().get(request, *args, **kwargs)
