from rest_framework import serializers

from masters.models import Master


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
