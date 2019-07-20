import string
from random import choice, shuffle

from django.db import models


from server.settings import DB_PREFIX
from server.settings import AUTH_USER_MODEL
from lib.modelmanager import ModelManager
from datamodels.customers.models import mm_Customer



class InviteRecordManager(ModelManager):

    Invite_Action_Enroll = 0
    Invite_Action_Buy = 1
    Invite_Action_Choice = (
        (Invite_Action_Enroll, '邀请注册'),
        (Invite_Action_Buy, '购买科目'),
    )

    def add_record(self, customer_id, invite_code=None, action_type=Invite_Action_Enroll, total_fee=None):
        if not invite_code:
            return
        inviter = mm_Customer.get(invite_code=invite_code)
        if action_type == self.Invite_Action_Enroll:
            rewards = 2.0
        else:
            rewards = total_fee * 0.1
        kwargs = {
            'inviter_id': inviter.id,
            'invited_id': customer_id,
            'action_type': action_type,
            'rewards': rewards
        }
        InviteRecord(**kwargs).save()
        mm_BlanceRecord.add_record(inviter.id, rewards, action_type)


class InviteRecord(models.Model):

    inviter = models.ForeignKey(
        'customers.Customer', related_name='inviters', on_delete=models.CASCADE, verbose_name='邀请人')
    invited = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='被邀请用户'
    )

    action_type = models.PositiveSmallIntegerField(choices=InviteRecordManager.Invite_Action_Choice,
                                                   default=InviteRecordManager.Invite_Action_Enroll,
                                                   verbose_name='类型')
    rewards = models.FloatField(default=0, verbose_name='提成')
    create_at = models.DateTimeField(auto_now_add=True)

    objects = InviteRecordManager()

    class Meta:
        db_table = DB_PREFIX + 'invite_record'


class CustomerBlanceManager(ModelManager):

    Action_Blance_In = 0
    Action_Blance_Out = 1
    Action_Blance_Choice = (
        (Action_Blance_In, '增加'),
        (Action_Blance_Out, '减少'),
    )

    def add_record(self, customer_id, amount, action_type=Action_Blance_In):

        record = self.filter(customer_id=customer_id).order_by('-create_at').first()
        if action_type == self.Action_Blance_In:
            if record:
                blance = record.blance + amount
                total_income = record.total_income + amount
                total_withdraw = record.total_withdraw
            else:
                blance = amount
                total_income = amount
                total_withdraw = 0
        else:
            if record:
                blance = record.blance - amount
                total_income = record.total_income
                total_withdraw = record.total_withdraw + amount

            else:
                return

        kwargs = {
            'customer_id': customer_id,
            'blance': blance,
            'amount': amount,
            'total_income': total_income,
            'total_withdraw': total_withdraw,
            'action_type': action_type
        }
        self.create(**kwargs)

    def get_blance(self, customer_id):
        return self.get_detail(customer_id)['blance']

    def get_detail(self, customer_id):
        record = self.filter(customer_id=customer_id).order_by('-create_at').first()
        detail_dict = {
            'blance': record.blance if record else 0,
            'total_income': record.total_income if record else 0,
            'total_withdraw': record.total_withdraw if record else 0,
        }
        return detail_dict


class BlanceRecord(models.Model):

    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='用户')
    amount = models.FloatField(default=0, verbose_name='操作数值')
    blance = models.FloatField(default=0, verbose_name='当前余额')
    total_income = models.FloatField(default=0, verbose_name='总收入金额')
    total_withdraw = models.FloatField(default=0, verbose_name='总提现金额')
    action_type = models.PositiveSmallIntegerField(choices=CustomerBlanceManager.Action_Blance_Choice,
                                                   default=CustomerBlanceManager.Action_Blance_In,
                                                   verbose_name='增加|减少')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = CustomerBlanceManager()

    class Meta:
        db_table = DB_PREFIX + 'blance_record'
        ordering = ['-create_at']

class WithDrawRecordManager(ModelManager):
    Status_Submited = 0
    Status_Done = 1
    Status_Refused = 2

    Status_Choice = (
        (Status_Submited, '已提交'),
        (Status_Done, '已提现'),
        (Status_Refused, '拒绝提现'),
    )


class WithDrawRecord(models.Model):

    customer = models.ForeignKey('customers.Customer', verbose_name='申请人', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(verbose_name='申请状态',
                                              choices=WithDrawRecordManager.Status_Choice,
                                              default=WithDrawRecordManager.Status_Submited)
    amount = models.PositiveIntegerField(verbose_name='数量', default=0)
    operator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='处理人')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    alipay_account = models.CharField(verbose_name='支付宝账号', max_length=20)

    objects = WithDrawRecordManager()

    class Meta:
        db_table = DB_PREFIX + 'withdraw_records'
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '提现申请管理'



mm_InviteRecord = InviteRecord.objects
mm_BlanceRecord = BlanceRecord.objects
mm_WithDrawRecord = WithDrawRecord.objects

