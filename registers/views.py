from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from main.pagination import StandardResultsSetPagination

from registers import serializers
from registers.exceptions import RegisterAlreadyStarted
from registers.filters import RegisterFilterSet, RegisterUserFilterSet
from registers.models import Register


started_before = openapi.Parameter('started_before', openapi.IN_QUERY, type=openapi.FORMAT_DATETIME,
                                   description='Фильтрует записи, которые начинаются ранее указанной даты')
started_after = openapi.Parameter('started_after', openapi.IN_QUERY, type=openapi.FORMAT_DATETIME,
                                  description='Фильтрует записи, которые начинаются позднее указанной даты')
master_id = openapi.Parameter('master_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Фильтрует записи, в которых мастер, id которого указан')
user_id = openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                            description='Фильтрует записи, в которых пользователь, id которого указан')


class RegisterListCreateView(generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.RegisterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RegisterFilterSet
    queryset = Register.objects.all()

    @swagger_auto_schema(manual_parameters=[started_before, started_after, master_id, user_id])
    def get(self, request, *args, **kwargs):
        """ Выводит все существующие записи """
        return super().get(request, *args, **kwargs)


class RegisterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RegisterSerializer

    def get_queryset(self):
        return Register.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        register = self.get_object()

        if register.start_at <= timezone.now():
            raise RegisterAlreadyStarted()

        return super().delete(request, *args, **kwargs)


class RegisterUserListView(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.RegisterSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RegisterUserFilterSet

    def get_queryset(self):
        return Register.objects.filter(user=self.request.user)

    @swagger_auto_schema(manual_parameters=[started_before, started_after, master_id])
    def get(self, request, *args, **kwargs):
        """ Возвращает все записи, пользователя, который совершает запрос """
        return super().get(request, *args, **kwargs)
