from rest_framework.exceptions import ValidationError


class NonWorkingTime(ValidationError):
    default_detail = 'You must specify working time'


class MasterIsBusy(ValidationError):
    default_detail = 'Master is busy at this time'
