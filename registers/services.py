from datetime import datetime

from django.conf import settings
from django.utils import timezone


class RegisterService:
    @staticmethod
    def check_is_working_time(time: datetime) -> bool:
        """
        Проверяет рабочее ли указанное время.
        Время рабочее, если:
        - Указанное время входит в рабочее время и имеет запас на работу до конца рабочего дня.
        - Указанное время входит в рабочие дни.

        :return: True если указанное время рабочее.
        """

        working_day_ends_at_hour_with_offset = settings.WORKING_DAY_ENDS_AT_HOUR - settings.REGISTER_LIFETIME

        is_working_condition = (
           time >= timezone.now()
           and
           time.weekday() not in settings.NON_WORKING_DAYS_OF_THE_WEEK
           and
           settings.WORKING_DAY_STARTS_AT_HOUR <= time.hour < working_day_ends_at_hour_with_offset
        )
        return is_working_condition
