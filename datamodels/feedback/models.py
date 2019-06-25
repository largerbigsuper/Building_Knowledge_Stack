from django.db import models

from server.settings import DB_PREFIX
from lib.modelmanager import ModelManager


class FeedBackManager(ModelManager):
    pass


class FeedBack(models.Model):
    customer = models.ForeignKey('customers.Customer', related_name='feedbacks', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='反馈内容', max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(verbose_name='状态', choices=ModelManager.Feedback_Status, default=ModelManager.Feedback_Unread)

    objects = FeedBackManager()

    class Meta:
        db_table = DB_PREFIX + 'feedback'
        verbose_name = '反馈管理'
        verbose_name_plural = '反馈管理'


mm_Feedback = FeedBack.objects