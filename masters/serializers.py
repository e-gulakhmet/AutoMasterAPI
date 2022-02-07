from rest_framework import serializers

from masters.models import Master


class MasterSerializer(serializers.ModelSerializer):
    registers_count = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = [
            'pk',
            'first_name',
            'second_name',
            'middle_name',
            'registers_count'
        ]
        read_only_fields = [
            'pk',
            'first_name',
            'second_name',
            'middle_name',
            'registers_count'
        ]

    @staticmethod
    def get_registers_count(instance: Master) -> int:
        return instance.registers.count()
