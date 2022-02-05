from rest_framework import generics

from main.pagination import StandardResultsSetPagination
from masters import serializers
from masters.models import Master


class MasterRetrieveView(generics.RetrieveAPIView):
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.all()


class MasterListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.MasterSerializer
    queryset = Master.objects.order_by('-pk')  # TODO: Добавить сортировку по количеству записей
    # TODO: Добавить фильтрацию отображения только свободных мастеров
    # TODO: Добавить сортировку по количеству записей
