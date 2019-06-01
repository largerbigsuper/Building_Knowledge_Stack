from django_filters import rest_framework as filters

from datamodels.questions.models import mm_Question

class AdminQuestionFilter(filters.FilterSet):

    class Meta:
        model = mm_Question.model
        fields = {
            'subject': ['exact'],
        }