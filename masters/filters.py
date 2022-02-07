from datetime import datetime

import django_filters

from registers.services import RegisterService


class MasterFilterSet(django_filters.rest_framework.FilterSet):
    free_at = django_filters.DateTimeFilter(method='filter_free_at')

    @staticmethod
    def filter_free_at(queryset, name, value: datetime):
        if not RegisterService.check_is_working_time(value):
            return queryset.none()
        return queryset.exclude_busy_masters_at_specified_time(value)

