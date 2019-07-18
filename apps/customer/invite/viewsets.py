from rest_framework import viewsets

from datamodels.invite.models import mm_InviteRecord
from apps.customer.invite.filters import CustomerInfiteFilter
from apps.customer.invite.serilizers import MyInviteRecordSerializer

class CustomerInviteRecordViewSet(viewsets.ModelViewSet):


    serializer_class = MyInviteRecordSerializer
    filter_class = CustomerInfiteFilter

    def get_queryset(self):
        return mm_InviteRecord.filter(inviter_id=self.request.user.customer.id)
