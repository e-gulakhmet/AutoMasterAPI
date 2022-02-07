import os.path
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MasterQuerySet(models.QuerySet):
    def exclude_busy_masters_at_specified_time(self, date_time: datetime):
        return self.exclude(
            registers__start_at__range=[date_time, date_time + timedelta(hours=settings.REGISTER_LIFETIME)]
        )


class MasterManager(models.Manager):
    def get_queryset(self):
        return MasterQuerySet(self.model, using=self._db)


class Master(models.Model):
    first_name = models.CharField(_('First name'), max_length=150)
    second_name = models.CharField(_('Second name'), max_length=150)
    middle_name = models.CharField(_('Middle name'), max_length=150, blank=True)
    avatar = models.ImageField(_('Avatar image'), default=os.path.join(settings.DEFAULT_ROOT, 'master_avatar.png'),
                               blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = MasterManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.second_name}'
