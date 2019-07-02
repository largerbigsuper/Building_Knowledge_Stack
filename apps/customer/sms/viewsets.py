from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.customer.sms.serializers import SMSSerializer
from lib.ali_sms import smsserver
from datamodels.sms.models import mm_SMSCode
from lib.exceptions import SMSExcecption


class CustomerSMSViewSet(mixins.CreateModelMixin, GenericViewSet):

    permission_classes = []
    authentication_classes = []
    serializer_class = SMSSerializer

    def create(self, request, *args, **kwargs):
        account = request.data.get('account')
        if not mm_SMSCode.can_get_new_code(tel=account):
            raise SMSExcecption('请过几分钟尝试')
        code = smsserver.gen_code()
        response = smsserver.send_sms(account, code)
        if response['Code'] == 'OK':
            # mm_SMSCode.add(account, code)
            mm_SMSCode.cache.set(account, code, 60 * 5)
            return Response()
        else:
            raise SMSExcecption(response['Message'])
