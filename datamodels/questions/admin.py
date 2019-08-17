from django.contrib import admin

from datamodels.questions.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Question._meta.fields]


