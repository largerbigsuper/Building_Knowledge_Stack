from apps.admin.questions.serializers import AdminQuestionSerializer, AdminQuestionCreateModifySerializer
from apps.admin.questions.filters import AdminQuestionFilter
from apps.base.viewsets import AdminModelViewSet
from datamodels.questions.models import mm_Question


class AdminQuestionViewSet(AdminModelViewSet):

    queryset = mm_Question.all()
    filter_class = AdminQuestionFilter
    
    def get_serializer_class(self):
        if self.request.method == 'GET': # 获取详情或列表的时候返回类型的Json结构
            return AdminQuestionSerializer
        else:
            return AdminQuestionCreateModifySerializer
