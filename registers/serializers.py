from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import serializers


from masters.models import Master
from masters.serializers import MasterSerializer
from registers.exceptions import MasterIsBusy, NonWorkingTime

from registers.models import Register
from registers.services import RegisterService


class RegisterCreateSerializer(serializers.ModelSerializer):
    """
    Запись можно создать, если:
    - Указанная дата входит в рабочее время и имеет запас на работу до конца рабочего дня.
    - Указанная дата входит в рабочие дни.
    - Указанный мастер не имеет записи на указанное время и имеет запас на работу до следующей записи.
    """

    master = MasterSerializer(read_only=True)

    class Meta:
        model = Register
        fields = [
            'pk',
            'start_at',
            'end_at',
            'master',
            'created_at',
        ]
        read_only_fields = [
            'pk',
            'end_at',
            'master',
            'created_at',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        start_at: datetime = attrs['start_at']
        master_pk = self.context['view'].kwargs['master_pk']

        if not RegisterService.check_is_working_time(start_at):
            raise NonWorkingTime()

        master = Master.objects.get(pk=master_pk)
        if Register.objects.filter(
                master=master,
                start_at__range=[start_at, start_at + timedelta(hours=settings.REGISTER_LIFETIME)],
                end_at__gte=start_at
        ).exists():
            raise MasterIsBusy()
        # if Register.objects.filter(
        #         master=master,
        #         start_at__lte=start_at,
        #         end_at__gte=start_at
        # ).exists():
        #     raise UnavailableTime()

        attrs['master'] = master
        attrs['user'] = self.context['request'].user
        return attrs
