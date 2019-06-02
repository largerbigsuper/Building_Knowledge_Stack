from apps.base.viewsets import CustomerReadOnlyModelViewSet, CustomerModelViewSet
from apps.customer.questions.filters import CustomerQuestionFilter
from apps.customer.questions.serializers import CustomerQuestionSerializer, CustomerQuestionRecordSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord


class CustomerQuestionViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerQuestionSerializer
    queryset = mm_Question.all()
    filter_class = CustomerQuestionFilter


class CustomerQuestionRecordViewSet(CustomerModelViewSet):
    """用户提交题目答案"""

    serializer_class = CustomerQuestionRecordSerializer
    filter_class = None
    
    def get_queryset(self):
        # mm_QuestionRecord.my_records(customer_id=self.request.session['cid'])
        return mm_QuestionRecord.my_records(customer_id=self.request.user.customer.id)
    
    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        # serrializer.data 在校验之后不能再修改， 不然要重新调用serializer.is_valid()
        q = serializer.validated_data['question']
        answer = serializer.validated_data['answer']
        upper_answer = [choice.upper() for choice in answer]
        is_correct = q.is_correct_answer(answer)
        serializer.validated_data['is_correct'] = is_correct
        serializer.validated_data['answer'] = upper_answer
        serializer.save()

