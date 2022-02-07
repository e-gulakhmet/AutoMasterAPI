from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def normalize_email(self, email_address):
        """ Normalize the email address by lower casing the domain part of it. """

        email_address = email_address or ''
        try:
            email_name, domain_part = email_address.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email_address = email_name.lower() + '@' + domain_part.lower()
        return email_address

    def create_user(self, email, password, **extra_fields):
        """ Create and save a User with the given email and password. """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password. """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('First name'), max_length=150)
    second_name = models.CharField(_('Second name'), max_length=150)
    middle_name = models.CharField(_('Middle name'), max_length=150, blank=True)

    car_model = models.CharField(_('Car model'), max_length=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email} - {self.get_full_name()}'

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.second_name}'
