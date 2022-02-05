from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserCreateSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    second_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    car_model = serializers.CharField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError(_('User already exist.'))

        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        return User.objects.create_user(email=email, password=password, **validated_data)


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'first_name',
            'second_name',
            'middle_name',
            'car_model',
        ]
        read_only_fields = [
            'pk',
            'email',
        ]
