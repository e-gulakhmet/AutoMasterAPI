from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users import serializers


class UserCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserRetrieveUpdateSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.process()
        return Response(status=status.HTTP_200_OK)