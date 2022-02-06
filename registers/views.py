from rest_framework import generics

from registers import serializers


class RegisterCreateView(generics.CreateAPIView):
    serializer_class = serializers.RegisterCreateSerializer
