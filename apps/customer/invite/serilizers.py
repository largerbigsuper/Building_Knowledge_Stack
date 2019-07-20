from rest_framework import serializers

from apps.base.serializers.customers import CustomerForeginKeySerializer

from datamodels.invite.models import mm_InviteRecord, mm_WithDrawRecord, mm_BlanceRecord

class MyInviteRecordSerializer(serializers.ModelSerializer):

    invited = CustomerForeginKeySerializer()

    class Meta:
        model = mm_InviteRecord.model
        fields = ['id', 'invited', 'action_type', 'rewards', 'create_at']


class CustomerBlanceRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_BlanceRecord.model
        fields = '__all__'


class CustomerWithDrawRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_WithDrawRecord.model
        fields = ('id', 'amount', 'status', 'create_at', 'alipay_account')
        read_only_fields = ('status', )
