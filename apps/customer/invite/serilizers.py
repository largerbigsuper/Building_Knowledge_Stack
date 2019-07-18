from rest_framework import serializers

from apps.base.serializers.customers import CustomerForeginKeySerializer

from datamodels.invite.models import mm_InviteRecord

class MyInviteRecordSerializer(serializers.ModelSerializer):

    invited = CustomerForeginKeySerializer()

    class Meta:
        model = mm_InviteRecord.model
        fields = ['id', 'invited', 'action_type', 'rewards', 'create_at']