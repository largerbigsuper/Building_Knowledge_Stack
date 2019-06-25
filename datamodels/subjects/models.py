import json
import time

from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from lib.modelmanager import ModelManager
from server.settings import DB_PREFIX, AlipaySettings
from lib import pay


class SubjectManager(ModelManager):

    def subject_by_level(self, level=0):
        return self.filter(level=level)


class Subject(MPTTModel):
    """报考类型"""

    name = models.CharField(max_length=20, verbose_name='报考类型')
    image = models.ImageField(blank=True, verbose_name='背景图')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    objects = SubjectManager()

    class MPTTMeta:
        order_insertion_by = ['level']

    class Meta:
        db_table = DB_PREFIX + 'subjects'

    def __str__(self):
        return self.name


class SubjectTermManager(ModelManager):
    pass


class SubjectTerm(models.Model):
    """报名批次"""

    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='批次说明')
    price = models.FloatField(default=0, verbose_name='价格（元）')
    price_info = models.TextField(blank=True, verbose_name='费用说明')
    subject_info = models.TextField(blank=True, verbose_name='课程介绍')
    status = models.PositiveSmallIntegerField(choices=ModelManager.Subject_Term_Status,
                                              default=ModelManager.Subject_Term_Status_OFF,
                                              verbose_name='可以报名/不可以报名')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = SubjectTermManager()

    class Meta:
        db_table = DB_PREFIX + 'subject_terms'

    def __str__(self):
        return self.name


class ApplicationManager(ModelManager):

    def add(self, customer_id, subject_term_id,
            union_trade_no, subject_term_name, total_amount, name, tel, id_number, id_card_front=None, id_card_back=None, status=ModelManager.Pay_Status_Unpaid):
        return self.create(customer_id=customer_id,
                           subject_term_id=subject_term_id,
                           union_trade_no=union_trade_no,
                           subject_term_name=subject_term_name,
                           total_amount=total_amount,
                           status=status,
                           name=name,
                           tel=tel,
                           id_number=id_number,
                           id_card_front=id_card_front,
                           id_card_back=id_card_back
                           )

    def create_alipay_order(self, customer_id, subject_term_id, name, tel, id_number, pay_from='APP', id_card_front=None, id_card_back=None):
        subject_term = mm_SubjectTerm.get(pk=subject_term_id)
        total_amount = subject_term.price
        subject = subject_term.name
        out_trade_no = pay.gen_union_trade_no()
        order = self.add(customer_id=customer_id,
                         subject_term_id=subject_term.id,
                         union_trade_no=out_trade_no,
                         subject_term_name=subject_term.name,
                         total_amount=total_amount,
                         name=name,
                         tel=tel,
                         id_number=id_number,
                         id_card_front=id_card_front,
                         id_card_back=id_card_back
                         )
        order_string = None
        if pay_from.upper() == 'APP':
            order_string = pay.alipay_serve.api_alipay_trade_app_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject,
                notify_url=AlipaySettings.VIRTUAL_SERVICE_NOTIFY_URI,
                timeout_express='15m'
            )
        return order_string

    def create_wechat_order(self, customer_id, subject_term_id, name, tel, id_number, pay_from='APP', spbill_create_ip=None, id_card_front=None, id_card_back=None):
        subject_term = mm_SubjectTerm.get(pk=subject_term_id)
        subject = subject_term.name
        total_amount = subject_term.price
        out_trade_no = pay.gen_union_trade_no(pay_type=2)
        order = self.add(customer_id=customer_id,
                         subject_term_id=subject_term.id,
                         union_trade_no=out_trade_no,
                         subject_term_name=subject_term.name,
                         total_amount=total_amount,
                         name=name,
                         tel=tel,
                         id_number=id_number,
                         id_card_front=id_card_front,
                         id_card_back=id_card_back
                         )
        order_string = None
        if pay_from.upper() == 'APP':
            order_string = pay.wechatpay_serve.unified_order(
                trade_type='APP',
                out_trade_no=out_trade_no,
                body=subject,
                total_fee=int(total_amount * 100),
                spbill_create_ip=spbill_create_ip
            )
        data = {}
        data['appid'] = order_string['appid']
        data['partnerid'] = order_string['mch_id']
        data['prepayid'] = order_string['prepay_id']
        data['noncestr'] = order_string['nonce_str']
        data['timestamp'] = str(int(time.time()))
        data['package'] = 'Sign=WXPay'
        sign = pay.wechatpay_serve.sign(data)
        data['sign'] = sign
        return data


class Application(models.Model):
    """报名记录"""

    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.DO_NOTHING,
        verbose_name='申请人')
    subject_term = models.ForeignKey(
        'subjects.SubjectTerm',
        on_delete=models.DO_NOTHING,
        verbose_name='报名批次')
    update_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pay_at = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    pay_type = models.PositiveSmallIntegerField(
        verbose_name='支付平台', choices=ApplicationManager.Pay_Type_Choice, default=ApplicationManager.Pay_Type_Wechat)
    status = models.PositiveSmallIntegerField(
        verbose_name='订单状态', choices=ApplicationManager.Pay_Status_Choice, default=ApplicationManager.Pay_Status_Unpaid)
    union_trade_no = models.CharField(
        verbose_name='内部订单号', max_length=100, unique=True, blank=True)
    trade_no = models.CharField(
        verbose_name='流水号', max_length=100, blank=True, null=True)
    subject_term_name = models.CharField(
        verbose_name='批次名', max_length=100, blank=True)
    total_amount = models.FloatField(verbose_name='总额', default=0)
    name = models.CharField(max_length=40, verbose_name='报名人')
    tel = models.CharField(max_length=11, verbose_name='联系电话')
    id_number = models.CharField(max_length=40, verbose_name='身份证号码')
    id_card_front = models.ImageField(blank=True, verbose_name='身份证正面')
    id_card_back = models.ImageField(blank=True, verbose_name='身份证反面')

    objects = ApplicationManager()

    class Meta:
        db_table = DB_PREFIX + 'applications'

    def __str__(self):
        return '<Application {pk}>'.format(pk=self.id)


class OrderManager(ModelManager):
    ORDER_STATU_UNPAY = 0
    ORDER_STATU_DONE = 1


mm_Subject = Subject.objects
mm_SubjectTerm = SubjectTerm.objects
mm_Application = Application.objects
