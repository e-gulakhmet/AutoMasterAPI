from django.contrib import admin

from masters.models import Master


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass
