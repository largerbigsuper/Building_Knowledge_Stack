from rest_framework import serializers

from apps.base.serializers.questions import BaseQuestionSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord


class CustomerQuestionSerializer(BaseQuestionSerializer):

    class Meta:
        model = mm_Question.model
        fields = ['id',  'subject', 'qtype', 'content', 'choices',
                  'images', 'answer', 'update_at', 'create_at']


class CustomerQuestionRecordSerializer(serializers.ModelSerializer):

    answer = serializers.ListField()
    # is_correct = serializers.IntegerField(source='is_correct', default=1)

    class Meta:
        model = mm_QuestionRecord.model
        fields = ['id', 'question', 'answer', 'exam',
                  'is_correct', 'update_at', 'create_at', 'customer']
        extra_kwargs = {
            'is_correct': {'default': mm_QuestionRecord.Answer_Result_Correct,
                           'read_only': True
                           }
        }
