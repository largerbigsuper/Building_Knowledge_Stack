from rest_framework import serializers

from apps.base.serializers.questions import BaseQuestionSerializer
from apps.base.serializers.subjects import BaseSubjectSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam


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


class CustomerExamSerializer(serializers.ModelSerializer):

    subject = BaseSubjectSerializer()
    questions = serializers.ListField()
    answer = serializers.ListField()
    result = serializers.JSONField()

    class Meta:
        model = mm_Exam.model
        fields = ['id', 'subject', 'questions', 'answer', 'result', 'create_at']


class CustomerExamCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_Exam.model
        fields = ['subject']