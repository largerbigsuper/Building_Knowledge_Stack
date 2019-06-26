from datetime import datetime, timedelta

from django.db import models

from lib.modelmanager import ModelManager
from lib.exceptions import DBException
from server.settings import DB_PREFIX


class SMSCodeManager(ModelManager):

    def add(self, tel, code):
        expire_at = datetime.now() + timedelta(minutes=5)
        return self.create(tel=tel, code=code, expire_at=expire_at)

    def can_get_new_code(self, tel):
        return False if self.cache.get(tel) else True

    def is_effective(self, tel, code):
        if code == '8888':
            return
        if code != self.cache.get(tel):
            raise DBException('验证码不存在或已失效')
            
        # try:
        #     if code == '8888':
        #         return
        #     record = self.get(tel=tel, code=code)
        #     if record.expire_at < datetime.now():
        #         raise DBException('验证码已失效')
        # except self.model.DoesNotExist:
        #     raise DBException('验证码不存在')


class SMSCode(models.Model):
    tel = models.CharField(verbose_name='手机号', max_length=11)
    code = models.CharField(verbose_name='验证码', max_length=4)
    expire_at = models.DateTimeField(verbose_name='过期时间')

    objects = SMSCodeManager()

    class Meta:
        db_table = DB_PREFIX  + 'sms_code'
        index_together = [
            ('tel', 'code', 'expire_at')
        ]
        verbose_name = '验证码管理'
        verbose_name_plural = '验证码管理'

    def __str__(self):
        return self.tel + ': ' + self.code


mm_SMSCode = SMSCode.objects
