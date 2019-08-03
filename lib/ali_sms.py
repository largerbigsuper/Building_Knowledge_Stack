import uuid
import random
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from server.settings import AliYunSMS

class SMSServer:

    def __init__(self):
        self.client = AcsClient(AliYunSMS.ACCESS_KEY_ID, AliYunSMS.ACCESS_KEY_SECRET, 'default')
    
    @staticmethod
    def gen_code():
        return ''.join(random.sample(list(map(str, range(10))), 4))

    def send_sms(self, phone, code):
        """发送单个验证码"""

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('TemplateCode', AliYunSMS.SMS_TEMPLATE_ID)
        request.add_query_param('SignName', AliYunSMS.SMS_TEMPLATE_NAME)
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('TemplateParam', json.dumps({"code": code if code else self.gen_code()}))
        request.add_body_params('OutId', uuid.uuid1())
        response = self.client.do_action(request)
        # b'{"Message":"OK","RequestId":"97FDD87D-5B50-4BFA-BF9C-CA24768A5FE0","BizId":"419112860178747080^0","Code":"OK"}'

        return json.loads(response.decode('utf-8'))
        
    def send_order_sms(self, phone, name):
        """发送单个验证码"""

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('TemplateCode', AliYunSMS.SMS_TEMPLATE_ID_ORDER)
        request.add_query_param('SignName', AliYunSMS.SMS_TEMPLATE_NAME_ORDER)
        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('TemplateParam', json.dumps({"name": name}))
        request.add_body_params('OutId', uuid.uuid1())
        response = self.client.do_action(request)
        # b'{"Message":"OK","RequestId":"97FDD87D-5B50-4BFA-BF9C-CA24768A5FE0","BizId":"419112860178747080^0","Code":"OK"}'

        return json.loads(response.decode('utf-8'))
        


smsserver = SMSServer()