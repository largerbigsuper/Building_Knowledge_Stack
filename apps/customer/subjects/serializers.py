from rest_framework import serializers

from apps.base.serializers.subjects import BaseSubjectTermSerializer
from datamodels.subjects.models import mm_SubjectTerm, mm_Application


class CustomerSubjectTermSerializer(BaseSubjectTermSerializer):

    class Meta:
        model = mm_SubjectTerm.model
        fields = ['id', 'subject', 'name', 'price', 'price_info', 'subject_info',
                  'status', 'update_at', 'create_at', 'rewards']


class CustomerSubmitApplicationSerializer(serializers.Serializer):
    """用户报名"""

    pay_from = serializers.CharField(default='APP')
    pay_type = serializers.IntegerField(default=0)
    name = serializers.CharField(max_length=40, required=True)
    tel = serializers.CharField(required=True)
    id_number = serializers.CharField(required=True)
    id_card_front = serializers.CharField(required=False)
    id_card_back = serializers.CharField(required=False)
    xxx_image = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class CustomerApplicationSerializer(serializers.ModelSerializer):

    subject_term = CustomerSubjectTermSerializer()

    class Meta:
        model = mm_Application.model
        fields = ['id', 'subject_term', 'update_at', 'create_at', 'pay_at',
        'pay_type', 'status', 
        'union_trade_no', 'subject_term_name', 'total_amount', 
        'name', 'tel', 'id_number',
        'id_card_front', 'id_card_back', 'email', 'xxx_image']
