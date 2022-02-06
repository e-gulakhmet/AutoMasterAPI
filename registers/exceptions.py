from rest_framework.exceptions import ValidationError


class NonWorkingTime(ValidationError):
    default_detail = 'You must specify working time'


class MasterIsBusy(ValidationError):
    default_detail = 'Master is busy at this time'


class RegisterAlreadyStarted(ValidationError):
    default_detail = 'You can\'t destroy already started registry'


class UserAlreadyHasRegisterAtTheSameTime(ValidationError):
    default_detail = 'You can\t has multiple registers at the same time'
