from rest_framework import serializers

from apps.base.serializers.questions import BaseQuestionSerializer
from apps.base.serializers.subjects import BaseSubjectSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam


class CustomerQuestionMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_Question.model
        fields = ['id']


class CustomerQuestionSerializer(BaseQuestionSerializer):

    default_answer = {
        'my_answer': [],
        'is_correct': 0
    }

    my_answer = serializers.SerializerMethodField()
    is_correct = serializers.SerializerMethodField()
    is_marked = serializers.SerializerMethodField()

    class Meta:
        model = mm_Question.model
        fields = ['id',  'subject', 'qtype', 'content', 'choices',
                  'images', 'answer', 'update_at', 'create_at', 'my_answer', 'is_correct', 'is_marked']

    def get_my_answer(self, obj):
        if obj:
            answer_dict = self.context['answer_dict']
            marked_list = self.context['marked_list']
            answer = answer_dict.get(obj.id, self.default_answer)
            return answer['my_answer']
        else:
            return []

    def get_is_correct(self, obj):
        if obj:
            answer_dict = self.context['answer_dict']
            answer = answer_dict.get(obj.id, self.default_answer)
            return answer['is_correct']
        else:
            return 0

    def get_is_marked(self, obj):
        if obj:
            marked_list = self.context['marked_list']
            return 1 if obj.id in marked_list else 0
        else:
            return 0


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
        fields = ['id', 'subject', 'questions',
                  'answer', 'result', 'create_at']


class CustomerExamCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_Exam.model
        fields = ['id', 'subject']
