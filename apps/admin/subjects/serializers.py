from rest_framework import serializers
from apps.base.serializers.subjects import BaseSubjectSerializer
from apps.base.serializers.customers import CustomerForeginKeySerializer
from datamodels.subjects.models import mm_SubjectTerm, mm_Application


class AdminSubjectTermSerializer(serializers.ModelSerializer):
    subject = BaseSubjectSerializer(read_only=True)

    class Meta:
        model = mm_SubjectTerm.model
        fields = ['id', 'subject', 'name', 'price', 'price_info', 'subject_info',
                  'status', 'update_at', 'create_at']


class AdminSubjectTermCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_SubjectTerm.model
        fields = ['id', 'subject', 'name', 'price', 'price_info', 'subject_info',
                  'status', 'update_at', 'create_at']


class AdminApplicationSerializer(serializers.ModelSerializer):

    customer = CustomerForeginKeySerializer()
    subject_term = AdminSubjectTermSerializer()

    class Meta:
        model = mm_Application.model
        fields = ['id', 'customer', 'subject_term', 'update_at', 'create_at']

    