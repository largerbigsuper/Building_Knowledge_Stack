from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from apps.base.viewsets import AdminModelViewSet
from apps.base.serializers.subjects import BaseSubjectSerializer
from apps.base.filters.subjects import BaseSubjectFilter
from apps.admin.subjects.serializers import AdminSubjectTermSerializer, AdminApplicationSerializer, AdminSubjectTermCreateSerializer
from apps.admin.subjects.filters import AdminSubjectTermFilter, AdminApplicationFilter

from datamodels.subjects.models import mm_Subject, mm_SubjectTerm, mm_Application


class AdminSubjectViewSet(AdminModelViewSet):
    """培训项目"""

    serializer_class = BaseSubjectSerializer
    queryset = mm_Subject.all()
    filter_class = BaseSubjectFilter

    @action(detail=True, methods=['POST'], serializer_class=AdminSubjectTermSerializer)
    def add_term(self, request, pk=None, format=None):
        subject = self.get_object()
        if not subject.level == 2:
            data = {'detail': '小类创建报名批次'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=subject)
            return Response()
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class AdminSubjectTermViewSet(AdminModelViewSet):
    """批次管理"""

    # serializer_class= AdminSubjectTermSerializer
    queryset = mm_SubjectTerm.all()
    filter_class = AdminSubjectTermFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AdminSubjectTermSerializer
        else:
            return AdminSubjectTermCreateSerializer


class AdminApplicationViewSet(AdminModelViewSet):
    """报名管理"""

    serializer_class = AdminApplicationSerializer
    queryset = mm_Application.all()
    filter_class = AdminApplicationFilter


