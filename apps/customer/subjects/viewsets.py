from apps.base.viewsets import CustomerReadOnlyModelViewSet
from apps.base.serializers.subjects import BaseSubjectSerializer
from apps.base.filters.subjects import BaseSubjectFilter
from datamodels.subjects.models import mm_Subject, mm_SubjectTerm, mm_Application
from apps.customer.subjects.serializers import CustomerSubjectTermSerializer
from apps.customer.subjects.filters import CustomerSubjectTermFilter


class CustomerSubjectViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = BaseSubjectSerializer
    queryset = mm_Subject.all()
    filter_class = BaseSubjectFilter


class CustomerSubjectermViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerSubjectTermSerializer
    queryset = mm_SubjectTerm.all()
    filter_class = CustomerSubjectTermFilter
    
