from rest_framework.exceptions import ValidationError


class PasswordsDoNotMatch(ValidationError):
    default_detail = 'Password mismatch.'
