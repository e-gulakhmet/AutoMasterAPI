from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Register(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='registers')
    master = models.ForeignKey('masters.Master', on_delete=models.CASCADE, related_name='registers')

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} - {self.user.email} to {self.master.get_full_name()}'

    # TODO: Добавить, автоматическое указание end_at
