from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response

from main.pagination import StandardResultsSetPagination

from registers import serializers
from registers.exceptions import RegisterAlreadyStarted, StartDateGreaterThanEndDate
from registers.models import Register
from registers.services import RegisterService


class RegisterListCreateView(generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.RegisterSerializer

    def get_queryset(self):
        return Register.objects.filter(user=self.request.user)


class RegisterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RegisterSerializer

    def get_queryset(self):
        return Register.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        register = self.get_object()

        if register.start_at <= timezone.now():
            raise RegisterAlreadyStarted()

        return super().delete(request, *args, **kwargs)


class RegisterMasterListView(generics.ListAPIView):
    serializer_class = serializers.RegisterSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Register.objects.filter(master_id=self.kwargs['master_pk'])


class RegisterFreeDateListView(generics.GenericAPIView):
    pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        now_date = timezone.now().date()
        start_date = self.kwargs['start_date'] if self.kwargs['start_date'] >= now_date else now_date
        end_date = self.kwargs['end_date']

        if end_date < start_date:
            raise StartDateGreaterThanEndDate()

        free_dates = RegisterService().get_free_dates(start_date, end_date)
        return Response(data=[date.strftime('%Y-%m-%d') for date in free_dates], status=status.HTTP_200_OK)
