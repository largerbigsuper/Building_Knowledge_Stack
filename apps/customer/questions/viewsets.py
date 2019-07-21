from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.viewsets import CustomerReadOnlyModelViewSet, CustomerModelViewSet
from apps.customer.questions.filters import CustomerQuestionFilter, CustomerQuestionRecordFilter
from apps.customer.questions.serializers import (CustomerQuestionSerializer,
                                                 CustomerQuestionRecordSerializer,
                                                 CustomerExamSerializer,
                                                 CustomerExamCreateSerializer,
                                                 CustomerQuestionMarkSerializer,
                                                 CustomerQuestionRecordListSerializer)
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam


class CustomerQuestionViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerQuestionSerializer
    queryset = mm_Question.all()
    filter_class = CustomerQuestionFilter

    def get_serializer_context(self):
        """返回该用户所有的做题记录和收藏记录
        """
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            answer_dcit = mm_QuestionRecord.my_records_dict(
                customer_id=self.request.user.customer.id)
            marked_list = mm_Question.get_marked_questions_list(
                customer_id=self.request.user.customer.id)
        else:
            answer_dcit = {}
            marked_list = []
        context['answer_dict'] = answer_dcit
        context['marked_list'] = marked_list
        return context

    @action(detail=True, methods=['post'], serializer_class=CustomerQuestionMarkSerializer)
    def add_mark(self, request, pk=None):
        """添加收藏
        """
        question = self.get_object()
        question.markers.add(request.user.customer)
        return Response()

    @action(detail=True, methods=['post'], serializer_class=CustomerQuestionMarkSerializer)
    def remove_mark(self, request, pk=None):
        """添加收藏
        """
        question = self.get_object()
        question.markers.remove(request.user.customer)
        return Response()

    @action(detail=False, methods=['get'])
    def mark_list(self, request):
        """收藏列表
        """
        queryset = request.user.customer.question_set.all()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomerQuestionRecordViewSet(CustomerModelViewSet):
    """用户提交题目答案"""

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerQuestionRecordSerializer
        else:
            return CustomerQuestionRecordListSerializer

    filter_class = CustomerQuestionRecordFilter

    def get_queryset(self):
        # mm_QuestionRecord.my_records(customer_id=self.request.session['cid'])
        return mm_QuestionRecord.my_records(customer_id=self.request.user.customer.id)

    def perform_create(self, serializer):
        # serrializer.data 在校验之后不能再修改， 不然要重新调用serializer.is_valid()
        question = serializer.validated_data['question']
        exam = serializer.validated_data.get('exam', None)
        answer = serializer.validated_data['answer']
        upper_answer = [choice.upper() for choice in answer]
        is_correct = question.is_correct_answer(answer)
        serializer.validated_data['is_correct'] = is_correct
        serializer.validated_data['answer'] = upper_answer
        defaults = {
            'is_correct': is_correct,
            'answer': upper_answer
        }
        mm_QuestionRecord.update_or_create(customer=self.request.user.customer,
                                           question=question,
                                           exam=exam,
                                           defaults=defaults)

        # serializer.save(customer=self.request.user.customer)


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
        exam = mm_Exam._gen_an_exam(
            customer_id=self.request.user.customer.id, subject_id=subject_id)
        serializer = CustomerExamSerializer(exam)
        questions = []
        for q in exam.questions:
            questions.append(mm_Question.get_question(q))
        serializer = self.serializer_class(exam)
        data = serializer.data.copy()
        data['questions'] = questions

        return Response(data=data)

    @action(detail=True, methods=['get'])
    def complete_exam(self, request, pk=None):
        """提交试卷"""
        exam = self.get_object()
        result = mm_Exam._gen_exam_result(exam=exam)
        serializer = self.serializer_class(result)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        exam = self.get_object()
        questions = []
        for q in exam.questions:
            questions.append(mm_Question.get_question(q))
        serializer = self.serializer_class(exam)
        data = serializer.data.copy()
        data['questions'] = questions
        return Response(data=data)
