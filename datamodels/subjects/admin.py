from django.contrib import admin

from datamodels.subjects.models import Subject, SubjectTerm, Application

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectTerm)
class SubjectTermAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


