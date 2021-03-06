import traceback
import string
from random import choice, shuffle

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
    invite_code = models.CharField(max_length=4, unique=True, blank=True, null=True, db_index=True, verbose_name='邀请码')

    class Meta:
        abstract = True


class CustomerManager(ModelManager):
    
    raw_string = list(string.ascii_letters + string.digits)

    # def create(self, **kwargs):
    #     pass

    def gen_code(self):
        code = ''
        for _ in range(4):
            code += choice(self.raw_string)
        return code

    def add(self, account, password, **kwargs):
        try:
            with transaction.atomic():
                user = self._add_user(account, password)
                customer = self.create(user=user, account=account, **kwargs)
                customer.save()
                self.cache.delete(account)
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

    def reset_password(self, account, password):
        """重置密码
        
        Arguments:
            cid {int} -- 用户id
        """
        customer = self.filter(account=account).first()
        user = User.objects.filter(id=customer.user.id).first()
        if user:
            user.set_password(password)
            user.save()
            self.cache.delete(account)

class Customer(CommonInfo):

    objects = CustomerManager()

    class Meta:
        db_table = DB_PREFIX + 'customers'
        ordering = ['-id']
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.account
    
    def set_invite_code(self):
        while True:
            if self.invite_code:
                break
            try:
                self.invite_code = mm_Customer.gen_code()
                self.save()
                break
            except:
                continue
        return self.invite_code

        
mm_Customer = Customer.objects

