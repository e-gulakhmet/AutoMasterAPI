from django.contrib import admin

from registers.models import Register


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_filter = (
        'master',
    )
