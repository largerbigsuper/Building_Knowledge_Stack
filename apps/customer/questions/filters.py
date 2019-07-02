from django_filters import rest_framework as filters

from datamodels.questions.models import mm_Question, mm_QuestionRecord

class CustomerQuestionFilter(filters.FilterSet):

    class Meta:
        model = mm_Question.model
        fields = {
            'subject': ['exact'],
            'qtype': ['exact'],
            'content': ['contains']
        }


class CustomerQuestionRecordFilter(filters.FilterSet):

    class Meta:
        model = mm_QuestionRecord.model
        fields = {
            'exam': ['exact'],
            'question__subject': ['exact'],
        }