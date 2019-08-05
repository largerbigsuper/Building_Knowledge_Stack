from django.contrib import admin

from datamodels.feedback.models import FeedBack

@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    pass
