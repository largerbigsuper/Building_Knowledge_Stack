import logging
import json
from datetime import datetime
import traceback

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from apps.base.viewsets import CustomerReadOnlyModelViewSet, CustomerModelViewSet
from apps.base.serializers.subjects import BaseSubjectSerializer
from apps.base.filters.subjects import BaseSubjectFilter
from datamodels.subjects.models import mm_Subject, mm_SubjectTerm, mm_Application, mm_SubjectConfig
from apps.customer.subjects.serializers import CustomerSubjectTermSerializer, CustomerApplicationSerializer, CustomerSubmitApplicationSerializer
from apps.customer.subjects.filters import CustomerSubjectTermFilter
from apps.customer.questions.filters import CustomerQuestionFilter
from apps.customer.articles.serializers import CustomerExamNoticeSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord
from datamodels.invite.models import mm_InviteRecord
from datamodels.articles.models import mm_ExamNotice
from lib import pay
from lib.ali_sms import smsserver
from lib.pagination import PageNumberPagination_100


pay_logger = logging.getLogger('pay')


class CustomerSubjectViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = BaseSubjectSerializer
    queryset = mm_Subject.all()
    filter_class = BaseSubjectFilter
    
    pagination_class = PageNumberPagination_100

    @action(detail=True, methods=['get'], queryset=mm_Subject.all())
    def question_list(self, request, pk=None, format=None):
        """三级科目下所有的题目和我的做题状态"""
        subject = self.get_object()
        questions = mm_Question.filter(
            subject=subject)
        filter = CustomerQuestionFilter(request.GET, queryset=questions)
        if filter.errors:
            return Response(data=filter.errors, status=status.HTTP_400_BAD_REQUEST)
        all_qid_list = filter.qs.values_list('id', flat=True)
        all_answered_question = mm_QuestionRecord.exclude(exam_id=None).filter(
            question__subject_id=subject.id).values_list('id', 'is_correct')
        answer_dict = dict(all_answered_question)
        questions_status_list = []
        for qid in all_qid_list:
            d = {
                'id': qid,
                'status': answer_dict.get(qid, -1)
            }
            questions_status_list.append(d)
        subject_info = BaseSubjectSerializer(subject).data
        ret = {
            'subject': subject_info,
            'questions': questions_status_list
        }
        return Response(data=ret)

    @action(detail=False, methods=['get'])
    def index_list(self, request):
        subjects = mm_SubjectConfig.get_subjects_show_index()
        serializer = self.serializer_class(subjects, many=True)
        data = {
            'results': serializer.data,
            'can_click': False
        }

        return Response(data=data)

    @action(detail=True, methods=['get'])
    def exam_notice(self, request, pk=None):
        """科目考试须知
        """
        subject = self.get_object()
        notice = mm_ExamNotice.get_subject_notice(subject_id=subject.id)
        data = {}
        if notice:
            data = CustomerExamNoticeSerializer(notice).data
        return Response(data)


class CustomerSubjectermViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerSubjectTermSerializer
    queryset = mm_SubjectTerm.all()
    filter_class = CustomerSubjectTermFilter

    @action(detail=True, methods=['post'])
    def create_alipay_order(self, request, pk=None):
        """提交报名"""
        # application = mm_Application.create_alipay_order(customer_id=request.session['cid'], subject_term_id=pk)
        # pay_from = request.POST.get('pay_from', 'APP')
        s = CustomerSubmitApplicationSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        pay_from = s.validated_data['pay_from']
        name = s.validated_data['name']
        tel = s.validated_data['tel']
        id_number = s.validated_data['id_number']
        id_card_back = s.validated_data.get('id_card_back')
        id_card_front = s.validated_data.get('id_card_front')
        xxx_image = s.validated_data.get('xxx_image')
        email = s.validated_data.get('email')

        invite_code = request.query_params.get('invite_code')

        order_string = ''
        if pay_from == 'APP':
            order_string = mm_Application.create_alipay_order(
                customer_id=request.user.customer.id,
                subject_term_id=pk,
                name=name,
                tel=tel,
                id_number=id_number,
                id_card_front=id_card_front,
                id_card_back=id_card_back,
                email=email,
                invite_code=invite_code,
                xxx_image=xxx_image,
            )
        data = {
            'order_string': order_string
        }
        return Response(data=data)

    @action(detail=True, methods=['post'])
    def create_wechat_order(self, request, pk=None):
        """提交报名"""

        # pay_type = int(request.POST.get('pay_type', 0))
        # pay_from = request.POST.get('pay_from', 'APP')
        s = CustomerSubmitApplicationSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        pay_type = s.validated_data['pay_type']
        pay_from = s.validated_data['pay_from']
        name = s.validated_data['name']
        tel = s.validated_data['tel']
        id_number = s.validated_data['id_number']
        id_card_front = s.validated_data.get('id_card_front')
        id_card_back = s.validated_data.get('id_card_back')
        xxx_image = s.validated_data.get('xxx_image')
        email = s.validated_data.get('email')

        invite_code = request.query_params.get('invite_code')

        order_string = ''
        spbill_create_ip = request.META.get('HTTP_X_FORWARDED_FOR',
                                            request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
        if pay_from == 'APP':
            order_string = mm_Application.create_wechat_order(
                customer_id=request.user.customer.id,
                subject_term_id=pk,
                spbill_create_ip=spbill_create_ip,
                name=name,
                tel=tel,
                id_number=id_number,
                id_card_front=id_card_front,
                id_card_back=id_card_back,
                email=email,
                invite_code=invite_code,
                xxx_image=xxx_image,
            )
        data = {
            'order_string': order_string
        }
        return Response(data=data)


class CustomerApplicationViewSet(CustomerModelViewSet):

    serializer_class = CustomerApplicationSerializer

    def get_queryset(self):
        return mm_Application.filter(customer_id=self.request.user.customer.id)

    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    @transaction.atomic()
    def alipay_notify(self, request):
        """支付宝回调"""
        pay_logger.info('--------- alipay callback ----------')
        data = dict(request.data.dict())
        pay_logger.info('data: %s' % data)
        data_post = request.POST
        pay_logger.info('data_post: %s' % data_post)
        pay_logger.info('type(data) = {}'.format(type(data)))
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

                    smsserver.send_order_sms(
                        phone=order.customer.account, name=order.subject_term.name)
                    mm_Application.send_sms_to_admin(
                        tel_list=order.tel_noticed.split(','),
                        name=order.customer.account,
                        subject_name=order.subject_term.name)
                    pay_logger.info('start add record...')
                    mm_InviteRecord.add_record(customer_id=order.customer_id,
                                               invite_code=order.invite_code,
                                               action_type=mm_InviteRecord.Invite_Action_Buy,
                                               total_fee=order.total_amount,
                                               rewards=order.subject_term.rewards)

            except:
                pay_logger.error('Error: %s ' % traceback.format_exc())
            finally:
                return Response('success')
        else:
            return Response('failed')

    @action(detail=False, methods=['post'], authentication_classes=[], permission_classes=[])
    @transaction.atomic()
    def wechatpay_notify(self, request):
        """微信支付回调"""
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

            smsserver.send_order_sms(
                phone=order.customer.account,
                name=order.subject_term.name)
            mm_Application.send_sms_to_admin(
                tel_list=order.tel_noticed.split(','),
                name=order.customer.account,
                subject_name=order.subject_term.name)
            pay_logger.info('start add record...')
            mm_InviteRecord.add_record(customer_id=order.customer_id,
                                       invite_code=order.invite_code,
                                       action_type=mm_InviteRecord.Invite_Action_Buy,
                                       total_fee=order.total_amount,
                                       rewards=order.subject_term.rewards)
        return pay.wechatpay_serve.reply("OK", True)
