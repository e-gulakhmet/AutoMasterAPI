from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response

from registers import serializers
from registers.exceptions import RegisterAlreadyStarted
from registers.models import Register


class RegisterCreateView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer


class RegisterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = Register.objects.all()

    def delete(self, request, *args, **kwargs):
        register = self.get_object()

        if register.start_at <= timezone.now():
            raise RegisterAlreadyStarted()

        return super().delete(request, *args, **kwargs)

