from django_filters import rest_framework as filtes

from datamodels.subjects.models import Subject

exact = 'exact'
contains = 'contains'
gt = 'gt'
lt = 'lt'


class BaseSubjectFilter(filtes.FilterSet):

    class Meta:
        model = Subject
        fields = {
            'name': [contains],
            'level': [exact],
            'parent': [exact],
        }