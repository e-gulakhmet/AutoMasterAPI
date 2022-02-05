from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from masters.models import Master
from users.models import User


class MasterSerializer(serializers.ModelSerializer):
    # TODO: Добавить поле количества записей мастера
    class Meta:
        model = Master
        fields = [
            'pk',
            'first_name',
            'second_name',
            'middle_name',
        ]
        read_only_fields = [
            'pk',
            'first_name',
            'second_name',
            'middle_name',
        ]
