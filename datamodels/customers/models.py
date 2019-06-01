import traceback

from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError

from server.settings import AUTH_USER_MODEL, DB_PREFIX
from lib.exceptions import DBException
from lib.modelmanager import ModelManager


class CommonInfo(models.Model):
    GENDER_UNSET = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICE = (
        (GENDER_UNSET, '未知'),
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女'),
    )

    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.CharField(max_length=40, unique=True, verbose_name='账号')
    # mini_openid = models.CharField(max_length=40, unique=True, null=True, blank=True, verbose_name='小程序账号')
    name = models.CharField(max_length=30, blank=True, verbose_name='昵称')
    age = models.PositiveSmallIntegerField('年龄', null=True, blank=True)
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, default=0)
    avatar_url = models.CharField('头像', max_length=300, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True


class CustomerManager(ModelManager):

    def add(self, account, password, **kwargs):
        try:
            with transaction.atomic():
                user = self._add_user(account, password)
                customer = self.create(user=user, account=account, **kwargs)
                customer.save()

                return customer
        except IntegrityError:
            raise DBException('账号已注册')
        except:
            msg = traceback.format_exc()
            raise DBException(msg)

    def _create_miniprogram_account(self, mini_openid):
        account = mini_openid
        password = self.Default_Password
        customer = self.add(account, password, mini_openid=mini_openid)
        return customer

    def get_customer_by_miniprogram(self, mini_openid):
        """通过小程序获取customer"""
        customer = self.filter(mini_openid=mini_openid).first()
        if customer:
            return customer
        else:
            customer = self._create_miniprogram_account(mini_openid)
            return customer

    @staticmethod
    def _add_user(account, password):
        user = User.objects.create_user(username=account, password=password)
        return user


class Customer(CommonInfo):

    objects = CustomerManager()

    class Meta:
        db_table = DB_PREFIX + 'customers'


mm_Customer = Customer.objects

