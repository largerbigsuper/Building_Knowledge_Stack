from django.db import models


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

class ModelManager(models.Manager, Const):
    
    Default_Password = '888888'
    


class BaseModel(models.Model):

    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True
