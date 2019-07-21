from django.contrib import admin

from datamodels.common.models import AppVersion


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    pass

