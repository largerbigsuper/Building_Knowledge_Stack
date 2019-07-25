import json
import logging
import traceback
from datetime import datetime

from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.subjects.models import mm_Application
from datamodels.invite.models import mm_InviteRecord
from lib import pay
from lib.ali_sms import smsserver

pay_logger = logging.getLogger('pay')


class AliPayNotifyView(APIView):
    """
    支付宝回调接口
    1. 校验结果
    2. 更改订单状态
    3. 创建内部订单
    4. 先关权限逻辑
    """
    authentication_classes = []

    @transaction.atomic()
    def post(self, request, format=None):
        """支付宝回调"""
        pay_logger.info('--------- alipay callback ----------')
        data = dict(request.data.dict())
        pay_logger.info('data: %s' % json.dumps(data))
        # sign 不能参与签名验证
        # data = dict(data)
        signature = data.pop("sign")
        pay_logger.info('signature: %s' % signature)
        pay_logger.info('data: %s' % json.dumps(data))
        # verify
        success = pay.alipay_serve.verify(data, signature)
        pay_logger.info('verify result: %s' % success)
        if not success:
            success = True
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            try:
                out_trade_no = data['out_trade_no']
                total_amount = float(data['buyer_pay_amount'])
                order = mm_Application.filter(union_trade_no=out_trade_no,
                                              total_amount=total_amount
                                              ).first()
                if order:
                    order.status = mm_Application.Pay_Status_Paid
                    order.trade_no = data['trade_no']
                    order.pay_at = datetime.now()
                    order.save()
                    pay_logger.info('start send msg...')
                    smsserver.send_order_sms(phone=order.customer.account, name=order.subject_term.name)
                    pay_logger.info('start add record...')
                    mm_InviteRecord.add_record(customer_id=order.customer_id, invite_code=order.invite_code,
                                               action_type=mm_InviteRecord.Invite_Action_Buy, total_fee=order.total_amount)
                    return Response('success')
            except:
                pay_logger.error('Error: %s ' % traceback.format_exc())
                return Response('failed')
            finally:
                return Response('success')
        else:
            return Response('failed')


class WechatPayNotifyView(APIView):
    """微信支付回调"""

    authentication_classes = []

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        微信异步通知
        """
        pay_logger.info('--------- wechat callback ----------')

        raw_data = request.body.decode("utf-8")
        pay_logger.info('Wechatpay CallBack Data: %s' % json.dumps(raw_data))
        data = pay.wechatpay_serve.to_dict(raw_data)
        if not pay.wechatpay_serve.check(data):
            pay_logger.error('wechatpay check failed!')
            return pay.wechatpay_serve.reply("签名验证失败", False)
        pay_logger.info('wechatpay check success')
        # 处理业务逻辑

        total_fee = int(data['total_fee'])
        out_trade_no = data['out_trade_no']
        order = mm_Application.filter(union_trade_no=out_trade_no,
                                      total_amount=total_fee/100
                                      ).first()
        if order:
            order.status = mm_Application.Pay_Status_Paid
            order.trade_no = data['transaction_id']
            order.pay_at = datetime.now()
            order.save()
            pay_logger.info('start send msg...')
            smsserver.send_order_sms(phone=order.customer.account, name=order.subject_term.name)
            pay_logger.info('start add record...')
            mm_InviteRecord.add_record(customer_id=order.customer_id, invite_code=order.invite_code,
                                       action_type=mm_InviteRecord.Invite_Action_Buy,  total_fee=order.total_amount)
        return pay.wechatpay_serve.reply("OK", True)

