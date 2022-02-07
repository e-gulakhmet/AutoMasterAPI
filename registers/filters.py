import django_filters


class RegisterFilterSet(django_filters.rest_framework.FilterSet):
    master_id = django_filters.NumberFilter('master_id')
    user_id = django_filters.NumberFilter('user_id')
    started = django_filters.DateTimeFromToRangeFilter('start_at')


class RegisterUserFilterSet(django_filters.rest_framework.FilterSet):
    master_id = django_filters.NumberFilter('master_id')
    started = django_filters.DateTimeFromToRangeFilter('start_at')