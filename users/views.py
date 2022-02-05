from rest_framework import generics, permissions

from users import serializers


class UserCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer
