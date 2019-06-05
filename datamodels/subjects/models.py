from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from lib.modelmanager import ModelManager
from server.settings import DB_PREFIX


class SubjectManager(ModelManager):
    
    def subject_by_level(self, level=0):
        return self.filter(level=level)

class Subject(MPTTModel):
    """报考类型"""

    name = models.CharField(max_length=20, verbose_name='报考类型')
    image = models.ImageField(blank=True, verbose_name='背景图')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    objects = SubjectManager()

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        db_table = DB_PREFIX + 'subjects'

    def __str__(self):
        return self.name


class SubjectTermManager(ModelManager):
    pass


class SubjectTerm(models.Model):
    """报名批次"""

    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='批次说明')
    price = models.FloatField(default=0, verbose_name='价格（元）')
    price_info = models.TextField(blank=True, verbose_name='费用说明')
    subject_info = models.TextField(blank=True, verbose_name='课程介绍')
    status = models.PositiveSmallIntegerField(choices=ModelManager.Subject_Term_Status,
                                              default=ModelManager.Subject_Term_Status_OFF,
                                              verbose_name='可以报名/不可以报名')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = SubjectTermManager()

    class Meta:
        db_table = DB_PREFIX + 'subject_terms'
    
    def __str__(self):
        return self.name


class ApplicationManager(ModelManager):

    pass


class Application(models.Model):
    """报名记录"""

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.DO_NOTHING,
        verbose_name='申请人')
    subject_term = models.ForeignKey(
        'subjects.SubjectTerm',
        on_delete=models.DO_NOTHING,
        verbose_name='报名批次')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = ApplicationManager()

    class Meta:
        db_table = DB_PREFIX + 'applications'


mm_Subject = Subject.objects
mm_SubjectTerm = SubjectTerm.objects
mm_Application = Application.objects
