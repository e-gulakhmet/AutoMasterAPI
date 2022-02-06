import os.path

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Master(models.Model):
    first_name = models.CharField(_('First name'), max_length=150)
    second_name = models.CharField(_('Second name'), max_length=150)
    middle_name = models.CharField(_('Middle name'), max_length=150, blank=True)
    avatar = models.ImageField(_('Avatar image'), default=os.path.join(settings.DEFAULT_ROOT, 'master_avatar.png'))

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.first_name} {self.second_name}'

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.second_name}'
