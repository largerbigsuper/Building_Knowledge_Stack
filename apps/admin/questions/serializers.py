from rest_framework import serializers

from apps.base.serializers.questions import BaseQuestionSerializer

from datamodels.questions.models import mm_Question

class AdminQuestionSerializer(BaseQuestionSerializer):

    class Meta:
        model = mm_Question.model
        fields = ['id',  'subject', 'qtype', 'content', 'choices', 'images', 'answer', 'update_at', 'create_at']


class AdminQuestionCreateModifySerializer(BaseQuestionSerializer):

    class Meta:
        model = mm_Question.model
        fields = ['id',  'subject', 'qtype', 'content', 'choices', 'images', 'answer', 'update_at', 'create_at']


