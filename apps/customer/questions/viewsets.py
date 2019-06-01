from apps.base.viewsets import CustomerReadOnlyModelViewSet
from apps.customer.questions.filters import CustomerQuestionFilter
from apps.customer.questions.serializers import CustomerQuestionSerializer
from datamodels.questions.models import mm_Question


class CustomerQuestionViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerQuestionSerializer
    queryset = mm_Question.all()
    filter_class = CustomerQuestionFilter

