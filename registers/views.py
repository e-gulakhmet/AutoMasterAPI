from django.utils import timezone
from rest_framework import generics

from main.pagination import StandardResultsSetPagination

from registers import serializers
from registers.exceptions import RegisterAlreadyStarted
from registers.models import Register


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
