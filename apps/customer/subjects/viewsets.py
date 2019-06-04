from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.viewsets import CustomerReadOnlyModelViewSet
from apps.base.serializers.subjects import BaseSubjectSerializer
from apps.base.filters.subjects import BaseSubjectFilter
from datamodels.subjects.models import mm_Subject, mm_SubjectTerm, mm_Application
from apps.customer.subjects.serializers import CustomerSubjectTermSerializer
from apps.customer.subjects.filters import CustomerSubjectTermFilter
from datamodels.questions.models import mm_Question, mm_QuestionRecord


class CustomerSubjectViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = BaseSubjectSerializer
    queryset = mm_Subject.all()
    filter_class = BaseSubjectFilter


    @action(detail=True, methods=['get'], queryset=mm_Subject.subject_by_level(2))
    def question_list(self, request, pk=None, format=None):
        """三级科目下所有的题目和我的做题状态"""
        subject = self.get_object()
        all_qid_list = mm_Question.filter(subject=subject).values_list('id', flat=True)
        all_answered_question = mm_QuestionRecord.exclude(exam_id=None).filter(question__subject_id=subject.id).values_list('id', 'is_correct')
        answer_dict = dict(all_answered_question)
        questions_status_list = []
        for qid in all_qid_list:            
            d = {
                'id': qid,
                'status': answer_dict.get(qid, -1)
            }
            questions_status_list.append(d)
        subject_info = BaseSubjectSerializer(subject).data
        ret = {
            'subject': subject_info,
            'questions': questions_status_list
        }
        return Response(data=ret)
    


class CustomerSubjectermViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerSubjectTermSerializer
    queryset = mm_SubjectTerm.all()
    filter_class = CustomerSubjectTermFilter
    