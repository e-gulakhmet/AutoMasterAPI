from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Register(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='registers')
    master = models.ForeignKey('masters.Master', on_delete=models.CASCADE, related_name='registers')

    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, default=None, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('master', 'start_at')

    def __str__(self):
        return f'{self.user.email} to {self.master.get_full_name()} at {self.start_at.isoformat()}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.end_at = self.start_at + timedelta(hours=settings.REGISTER_LIFETIME)
        super().save()
