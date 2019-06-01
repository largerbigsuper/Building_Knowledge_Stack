from django_filters import rest_framework as filters

from datamodels.questions.models import mm_Question

class CustomerQuestionFilter(filters.FilterSet):

    class Meta:
        model = mm_Question.model
        fields = {
            'subject': ['exact'],
        }