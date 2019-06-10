from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.viewsets import CustomerReadOnlyModelViewSet, CustomerModelViewSet
from apps.customer.questions.filters import CustomerQuestionFilter, CustomerQuestionRecordFilter
from apps.customer.questions.serializers import CustomerQuestionSerializer, CustomerQuestionRecordSerializer, CustomerExamSerializer, CustomerExamCreateSerializer
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam


class CustomerQuestionViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerQuestionSerializer
    queryset = mm_Question.all()
    filter_class = CustomerQuestionFilter


class CustomerQuestionRecordViewSet(CustomerModelViewSet):
    """用户提交题目答案"""

    serializer_class = CustomerQuestionRecordSerializer
    filter_class = CustomerQuestionRecordFilter
    # queryset = mm_QuestionRecord.all()
    def get_queryset(self):
        # mm_QuestionRecord.my_records(customer_id=self.request.session['cid'])
        return mm_QuestionRecord.my_records(customer_id=self.request.user.customer.id)

    def perform_create(self, serializer):
        # serrializer.data 在校验之后不能再修改， 不然要重新调用serializer.is_valid()
        q = serializer.validated_data['question']
        answer = serializer.validated_data['answer']
        upper_answer = [choice.upper() for choice in answer]
        is_correct = q.is_correct_answer(answer)
        serializer.validated_data['is_correct'] = is_correct
        serializer.validated_data['answer'] = upper_answer
        serializer.save()


class CustomerExamViewSet(CustomerModelViewSet):

    serializer_class = CustomerExamSerializer
    
    def get_queryset(self):
        return mm_Exam.filter(customer=self.request.user.customer)
        # return mm_Exam.filter(customer_id=self.request.session['cid'])
    
    @action(detail=False, methods=['post'], serializer_class=CustomerExamCreateSerializer)
    def create_exam(self, request):
        """创建考试"""
        params = self.serializer_class(data=request.data)
        params.is_valid(raise_exception=True)
        subject_id = params.validated_data['subject'].id
        exam = mm_Exam._gen_an_exam(customer_id=self.request.user.customer.id, subject_id=subject_id)
        serializer = CustomerExamSerializer(exam)
        
        return Response(data=serializer.data)

    @action(detail=True, methods=['get'])
    def complete_exam(self, request, pk=None):
        """提交试卷"""
        exam = self.get_object()
        result = mm_Exam._gen_exam_result(exam=exam)
        serializer = self.serializer_class(result)
        return Response(serializer.data)
    