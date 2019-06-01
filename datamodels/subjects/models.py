from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from lib.modelmanager import ModelManager
from server.settings import DB_PREFIX


class SubjectManager(ModelManager):
    pass


class Subject(MPTTModel):
    """报考类型"""

    name = models.CharField(max_length=20, verbose_name='报考类型')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    objects = SubjectManager()

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        db_table = DB_PREFIX + 'subjects'

    def __str__(self):
        return self.name


mm_Subject = Subject.objects