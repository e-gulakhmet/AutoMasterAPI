from rest_framework import generics, permissions, status
from rest_framework.response import Response

from users import serializers


class UserCreateView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer

    def post(self, request, *args, **kwargs):
        """ Создает нового пользователя по указанным данным """
        return super().post(request, *args, **kwargs)


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserRetrieveUpdateSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """ Возвращает информацию о пользователе, которые делает запрос """
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ Обновляет указанные данные пользователя """
        return super().update(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        Сравнивает указанный старый пароль с паролем пользователя, если совпадает,
        то меняет на указанный новый пароль
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.process()
        return Response(status=status.HTTP_200_OK)