# import requests
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from apps.customer.customers.serilizers import (CustomerProfileSerializer,
                                                 LoginSerializer,
                                                 MiniprogramLoginSerializer,
                                                 RegisterSerializer,
                                                 PasswordSerializer,
                                                 )
from datamodels.customers.models import mm_Customer
from datamodels.sms.models import mm_SMSCode
from datamodels.invite.models import mm_InviteRecord
from server import settings
from lib.common import common_logout, customer_login
from lib.qiniucloud import QiniuService


class CustomerViewSet(viewsets.ModelViewSet):

    permission_classes = []
    serializer_class = CustomerProfileSerializer
    queryset = mm_Customer.all()
    

    # @csrf_exempt
    # @action(methods=['post'], detail=False, serializer_class=MiniprogramLoginSerializer, permission_classes=[])
    # def login_miniprogram(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     code = serializer.validated_data['code']
    #     wx_res = requests.get(settings.MinprogramSettings.LOGIN_URL + code)
    #     ret_json = wx_res.json()
    #     if 'openid' not in ret_json:
    #         return Response(data=ret_json, status=status.HTTP_400_BAD_REQUEST)
    #     openid = ret_json['openid']
    #     # session_key = ret_json['session_key']
    #     # unionid = ret_json.get('session_key')
    #     customer = mm_Customer.get_customer_by_miniprogram(openid)
    #     customer_login(request, customer.user)
    #     token, _ = Token.objects.get_or_create(user=customer.user)
    #     data = {
    #         'id': customer.id,
    #         'user_id': customer.user.id,
    #         'name': customer.name,
    #         'token': token.key,
    #     }
    #     return Response(data=data)

    @action(detail=False, methods=['post'], serializer_class=RegisterSerializer)
    def enroll(self, request):
        """注册"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        invite_code = serializer.validated_data.pop('invite_code', None)
        code = serializer.validated_data['code']
        mm_SMSCode.is_effective(account, code)
        customer = mm_Customer.add(account=account, password=password)
        mm_InviteRecord.add_record(customer_id=customer.id, invite_code=invite_code)
        return Response(data={'account': account})

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer, authentication_classes=[])
    def login(self, request):
        """登录"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        customer = mm_Customer.filter(account=account).first()
        if customer:
            user = authenticate(request, username=account, password=password)
            if user:
                customer_login(request, user)
                serailizer = CustomerProfileSerializer(customer)
                token, _ = Token.objects.get_or_create(user=user)
                data = serailizer.data
                data['token'] = token.key
                return Response(data=data)
            else:
                return Response(data={'detail': '账号或密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'detail': '账号不存在'}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def logout(self, request):
        """退登"""

        common_logout(request)
        return Response()

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """个人信息"""
        
        if request.method == 'GET':
            serializer = self.serializer_class(request.user.customer)
            return Response(data=serializer.data)
        else:
            serializer = self.serializer_class(request.user.customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated,])
    def qiniutoken(self, request):
        """获取七牛token
        """
        file_type = request.query_params.get('file_type', 'image')
        bucket_name = QiniuService.get_bucket_name(file_type)
        token = QiniuService.gen_app_upload_token(bucket_name)
        data = {'token': token}
        return Response(data=data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated,])
    def get_invite_code(self, request):
        """获取七牛token
        """
        invite_code = request.user.customer.set_invite_code()
        data = {'invite_code': invite_code}
        return Response(data=data)

    @action(detail=False, methods=['post'], permission_classes=[], serializer_class=PasswordSerializer)
    def reset_password(self, request):
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        code = serializer.validated_data['code']
        _code = mm_SMSCode.cache.get(account)
        if _code == code:
            mm_Customer.reset_password(account, password)
            return Response()
        else:
            data = {
                'detail': '验证码错误'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        