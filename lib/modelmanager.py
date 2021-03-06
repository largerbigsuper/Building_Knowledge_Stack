from django.db import models
from django.core.cache import cache


class Const(object):
    # 常量说明

    Subject_Term_Status_OFF = 0
    Subject_Term_Status_ON = 1
    Subject_Term_Status = (
        (Subject_Term_Status_OFF, '不可以报名'),
        (Subject_Term_Status_ON, '可以报名'),
    )

    Question_Type_Danxuanti = 0
    Question_Type_Duouanti = 1
    Question_Type_Panduanti = 2

    Question_Type = (
        (Question_Type_Danxuanti, '单选题'),
        (Question_Type_Duouanti, '多选题'),
        (Question_Type_Panduanti, '判断题'),
    )

    Answer_Result_Wrong = 0
    Answer_Result_Correct = 1
    Answer_Result = (
        (Answer_Result_Wrong, '错误'),
        (Answer_Result_Correct, '正确')
    )
    
    Publish_Unpublish = 0
    Publish_Published = 1

    Publish_Status = (
        (Publish_Unpublish, '未发布'),
        (Publish_Published, '已发布'),
    )

    Pay_Status_Unpaid = 0
    Pay_Status_Paid = 1

    Pay_Status_Choice = (
        (Pay_Status_Unpaid, '未付款'),
        (Pay_Status_Paid, '已付款')
    )

    Pay_Type_Wechat = 0
    Pay_Type_Alipay = 1
    Pay_Type_Choice = (
        (Pay_Type_Wechat, '微信支付'),
        (Pay_Type_Alipay, '支付宝')
    )

    Tag_AD_Question = 1
    Tag_AD_Application = 2
    Tag_Notice_Question = 3
    Tag_Notice_Application = 4
    Tag_Choice = (
        (Tag_AD_Question, '题库广告'),
        (Tag_AD_Application, '报名广告'),
        (Tag_Notice_Application, '题库通知'),
        (Tag_Notice_Application, '报名通知'),
    )

    Feedback_Unread = 0
    Feedback_accepted = 1

    Feedback_Status = (
        (Feedback_Unread, '未处理'),
        (Feedback_accepted, '已处理')
    )


class ModelManager(models.Manager, Const):
    
    Default_Password = '888888'
    cache = cache
    


class BaseModel(models.Model):

    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True
