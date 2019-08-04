from django.contrib import admin

from datamodels.articles.models import Tag, Article, ExamNotice


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(ExamNotice)
class ExamNoticeAdmin(admin.ModelAdmin):
    pass
