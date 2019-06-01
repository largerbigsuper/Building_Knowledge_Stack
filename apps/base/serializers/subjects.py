from rest_framework import serializers

from datamodels.subjects.models import mm_Subject


class BaseSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_Subject.model
        fields = ['id', 'parent', 'name', 'level']


class BaseSubjectTermSerializer(serializers.ModelSerializer):
    subject = BaseSubjectSerializer(read_only=True)
