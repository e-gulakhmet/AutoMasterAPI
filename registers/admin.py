from django.contrib import admin

from registers.models import Register


@admin.register(Register)
class UserAdmin(admin.ModelAdmin):
    pass
