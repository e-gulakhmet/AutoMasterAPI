from datetime import datetime, date, timedelta

from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from registers.models import Register


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

    @staticmethod
    def get_date_between(start: date, end: date) -> list[date]:
        delta = end - start  # as timedelta
        days = [start + timedelta(days=i) for i in range(delta.days + 1)]
        return days

    @staticmethod
    def exclude_weekend_dates(dates: list[date]) -> list[date]:
        return [d for d in dates if d.weekday() not in settings.NON_WORKING_DAYS_OF_THE_WEEK]

    @staticmethod
    def exclude_busy_dates(dates: list[date]) -> list[date]:
        times_per_days = {}
        for d in dates:
            key = d.isoformat()
            if times_per_days.get(key):
                times_per_days[key] += 1
            else:
                times_per_days[key] = 0

        dates

        for d, times in times_per_days:
            if times < settings.MAX_REGISTERS_TIMES_IN_DAY:
                continue



        return [d for d in dates if d.weekday() not in settings.NON_WORKING_DAYS_OF_THE_WEEK]

    def get_free_dates(self, start_date: date, end_date: date) -> list[date]:
        busy_dates = Register.objects \
            .filter(start_at__gte=start_date, end_at__lte=end_date) \
            .values('start_at__year', 'start_at__month', 'start_at__day') \
            .annotate(times_in_day=Count('*')) \
            .exclude(times_in_day__lt=settings.MAX_REGISTERS_TIMES_IN_DAY)
        busy_dates = {date(d['start_at__year'], d['start_at__month'], d['start_at__day']) for d in busy_dates}

        dates_between = set(self.get_date_between(start_date, end_date))

        free_dates = list(dates_between - busy_dates)
        free_dates = self.exclude_weekend_dates(free_dates)
        return sorted(free_dates)


