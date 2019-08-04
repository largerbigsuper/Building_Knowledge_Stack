from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from lib.modelmanager import ModelManager
from server.settings import DB_PREFIX


class TagManager(ModelManager):
    pass


class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=20, unique=True)
    level = models.PositiveIntegerField(verbose_name='排序值', default=0)

    objects = TagManager()

    class Meta:
        db_table = DB_PREFIX + 'tags'
        ordering = ['-level', '-id']
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return '<Tag {pk}> {name}'.format(pk=self.id, name=self.name)


class ArticleManager(ModelManager):
    
    def published(self):
        return self.filter(status=self.Publish_Published)


class Article(models.Model):

    headline = models.CharField(verbose_name='标题', max_length=200, db_index=True)
    image = models.ImageField(verbose_name='背景图', blank=True)
    # content = models.TextField(verbose_name='正文', max_length=10000)
    content = RichTextUploadingField(verbose_name='正文', max_length=10000)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    status = models.PositiveSmallIntegerField(verbose_name='是否发布', choices= ArticleManager.Publish_Status, default=ArticleManager.Publish_Unpublish)
    tags = models.ManyToManyField('Tag', blank=True)
    
    objects = ArticleManager()

    class Meta:
        db_table = DB_PREFIX + 'articles'
        ordering = ['-create_at', '-id']
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return '<Article: {pk}> {title}'.format(pk=self.id, title=self.headline)

class ExamNoticeManager(ModelManager):
    
    def published(self):
        return self.filter(status=self.Publish_Published)


class ExamNotice(models.Model):

    headline = models.CharField(verbose_name='标题', max_length=200, db_index=True)
    image = models.ImageField(verbose_name='背景图', blank=True)
    # content = models.TextField(verbose_name='正文', max_length=10000)
    content = RichTextUploadingField(verbose_name='正文', max_length=10000)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    status = models.PositiveSmallIntegerField(verbose_name='是否发布', choices= ArticleManager.Publish_Status, default=ArticleManager.Publish_Unpublish)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, verbose_name='科目')

    objects = ExamNoticeManager()

    class Meta:
        db_table = DB_PREFIX + 'exam_notices'
        ordering = ['-create_at', '-id']
        verbose_name = '考前说明'
        verbose_name_plural = '考前说明'

    def __str__(self):
        return '<ExamNotice: {pk}> {title}'.format(pk=self.id, title=self.headline)


mm_Tag = Tag.objects
mm_Article = Article.objects
mm_ExamNotice = ExamNotice.objects