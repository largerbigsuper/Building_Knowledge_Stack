from rest_framework import serializers

from apps.base.serializers.subjects import BaseSubjectTermSerializer
from datamodels.subjects.models import mm_SubjectTerm, mm_Application


class CustomerSubjectTermSerializer(BaseSubjectTermSerializer):

    class Meta:
        model = mm_SubjectTerm.model
        fields = ['id', 'subject', 'name', 'price', 'price_info', 'subject_info',
                  'status', 'update_at', 'create_at']


class CustomerSubmitApplicationSerializer(serializers.Serializer):
    """用户报名"""

    pay_type = serializers.IntegerField()


class CustomerApplicationSerializer(serializers.ModelSerializer):

    subject_term = CustomerSubjectTermSerializer()

    class Meta:
        model = mm_Application.model
        fields = ['id', 'subject_term', 'update_at', 'create_at', 'pay_at',
        'pay_type', 'status', 
        'union_trade_no', 'subject_term_name', 'total_amount']
