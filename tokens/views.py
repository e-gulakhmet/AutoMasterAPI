from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from tokens.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSlidingSerializer,
    TokenRefreshSerializer,
    TokenRefreshSlidingSerializer
)


class TokenObtainPairView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """ Генерирует jwt токен для пользователя, данные которого были указаны """
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenViewBase):
    permission_classes = [AllowAny]
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        Принимает refresh jwt токен и возвращает access jwt токен,
        если токен обновления действителен.
        """
        return super().post(request, *args, **kwargs)


class LoginCheckView(APIView):
    def post(self, request, *args, **kwargs):
        """ Проверяет jwt токен, который указан в headers """
        return Response(status=status.HTTP_200_OK)
