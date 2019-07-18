import string
from random import choice, shuffle

from django.db import models

from server.settings import DB_PREFIX
from lib.modelmanager import ModelManager
from datamodels.customers.models import mm_Customer


class InviteRecordManager(ModelManager):

    Invite_Action_Enroll = 0
    Invite_Action_Buy = 1
    Invite_Action_Choice = (
        (Invite_Action_Enroll, '邀请注册'),
        (Invite_Action_Buy, '购买科目'),
    )

    def add_record(self, customer_id, invite_code=None, action_type=Invite_Action_Enroll):
        if not invite_code:
            return
        inviter = mm_Customer.get(invite_code=invite_code)
        kwargs = {
            'inviter_id': inviter.id,
            'invited_id': customer_id,
            'action_type': action_type
        }
        InviteRecord(**kwargs).save()



class InviteRecord(models.Model):

    inviter = models.ForeignKey(
        'customers.Customer', related_name='inviters',on_delete=models.CASCADE, verbose_name='邀请人')
    invited = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE, verbose_name='被邀请用户'
    )

    action_type = models.PositiveSmallIntegerField(choices=InviteRecordManager.Invite_Action_Choice,
                                                   default=InviteRecordManager.Invite_Action_Enroll,
                                                   verbose_name='类型')
    create_at = models.DateTimeField(auto_now_add=True)

    objects = InviteRecordManager()

    class Meta:
        db_table = DB_PREFIX + 'invite_code'


mm_InviteRecord = InviteRecord.objects
