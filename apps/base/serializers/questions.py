from rest_framework import serializers

from apps.base.serializers.subjects import BaseSubjectSerializer

class BaseQuestionSerializer(serializers.ModelSerializer):

    subject = BaseSubjectSerializer(read_only=True)
    choices = serializers.ListField()
    images = serializers.ListField()
    answer = serializers.ListField()


