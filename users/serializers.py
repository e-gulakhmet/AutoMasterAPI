from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.exceptions import PasswordsDoNotMatch
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

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        return User.objects.create_user(email=email, password=password, **validated_data)

    def update(self, instance, validated_data):
        pass


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    second_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)
    car_model = serializers.CharField(required=False)

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


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context['request'].user

        if not user.check_password(attrs.get('password')):
            raise PasswordsDoNotMatch({'password': 'Wrong password'})

        attrs['user'] = self.context['request'].user
        return attrs

    def process(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
