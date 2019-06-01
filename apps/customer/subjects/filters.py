from django_filters import rest_framework as filters

from datamodels.subjects.models import SubjectTerm, Application


class CustomerSubjectTermFilter(filters.FilterSet):

    class Meta:
        model = SubjectTerm
        fields = {
            'subject': ['exact'],
            'name': ['contains']
        }


class CustomerApplicationFilter(filters.FilterSet):

    class Meta:
        model = Application
        fields = {
            'customer': ['exact'],
            'customer__name': ['contains'],
            'subject_term': ['exact'],
            'update_at': ['gt', 'lt'],
            'create_at': ['gt', 'lt'],
        }