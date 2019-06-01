from django_filters import rest_framework as filters

from datamodels.subjects.models import SubjectTerm, Application


class AdminSubjectTermFilter(filters.FilterSet):

    class Meta:
        model = SubjectTerm
        fields = {
            'subject': ['exact'],
            'name': ['contains']
        }


class AdminApplicationFilter(filters.FilterSet):

    class Meta:
        model = Application
        fields = {
            'customer': ['exact'],
            'customer__name': ['contains'],
            'subject_term': ['exact'],
            'update_at': ['gt', 'lt'],
            'create_at': ['gt', 'lt'],
        }