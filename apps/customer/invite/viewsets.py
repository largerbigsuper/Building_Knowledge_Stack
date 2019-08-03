from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from datamodels.invite.models import mm_InviteRecord, mm_WithDrawRecord, mm_BlanceRecord
from apps.customer.invite.filters import CustomerInfiteFilter
from apps.customer.invite.serilizers import MyInviteRecordSerializer, CustomerWithDrawRecordSerializer, CustomerBlanceRecordSerializer


class CustomerInviteRecordViewSet(viewsets.ModelViewSet):

    serializer_class = MyInviteRecordSerializer
    filter_class = CustomerInfiteFilter

    def get_queryset(self):
        return mm_InviteRecord.filter(inviter_id=self.request.user.customer.id)


class CustomerBlanceRecordViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerBlanceRecordSerializer

    def get_queryset(self):
        return mm_BlanceRecord.filter(customer_id=self.request.user.customer.id)

    @action(methods=['get'], detail=False)
    def detail_info(self, request):
        customer_id = request.user.customer.id
        # invited_count = mm_InviteRecord.filter(inviter_id=request.user.customer.id).count()
        data = mm_BlanceRecord.get_detail(customer_id=request.user.customer.id)

        return Response(data=data)


class CustomerWithDrawRecordViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerWithDrawRecordSerializer

    def get_queryset(self):
        return mm_WithDrawRecord.filter(customer_id=self.request.user.customer.id)

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.user.customer.id)

    def create(self, request, *args, **kwargs):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        amount = serailizer.validated_data['amount']
        if amount > mm_BlanceRecord.get_blance(request.user.customer.id):
            data = {
                'detail': '余额不足'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().create(request, *args, **kwargs)
