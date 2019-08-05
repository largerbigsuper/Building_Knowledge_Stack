from django.db import models

from server.settings import DB_PREFIX
from lib.modelmanager import ModelManager


class AppVersionManager(ModelManager):

    OS_TYPE_IOS = 0
    OS_TYPE_ANDROID = 1
    OS_TYPE_CHOICE = (
        (OS_TYPE_IOS, 'ios'),
        (OS_TYPE_ANDROID, 'android')
    )

    STATUS_IN_TEST = 0
    STATUS_PUBLISHED = 1
    APP_VERSION_STATUS_CHOICE = (
        (STATUS_IN_TEST, '测试中'),
        (STATUS_PUBLISHED, '已发布')
    )

    def published_versions(self):
        return self.filter(status=self.STATUS_PUBLISHED)

    def get_latest_version(self, os_type):
        return self.published_versions().filter(os_type=os_type).first()


class AppVersion(models.Model):

    os_type = models.PositiveSmallIntegerField(choices=AppVersionManager.OS_TYPE_CHOICE,
                                               default=AppVersionManager.OS_TYPE_IOS,
                                               verbose_name='操作系统')
    code = models.CharField(max_length=4, verbose_name='版本号')
    description = models.CharField(max_length=500, blank=True, verbose_name='简要描述')
    status = models.PositiveSmallIntegerField(choices=AppVersionManager.APP_VERSION_STATUS_CHOICE,
                                              default=AppVersionManager.STATUS_IN_TEST,
                                              verbose_name='测试中|已发布')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = AppVersionManager()

    class Meta:
        db_table = DB_PREFIX + 'app_version'
        ordering = ['-create_at']
        verbose_name = 'App版本'
        verbose_name_plural = 'App版本'


mm_AppVersion = AppVersion.objects
