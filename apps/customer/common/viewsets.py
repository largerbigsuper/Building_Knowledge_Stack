from rest_framework.decorators import action
from rest_framework.response import Response

from apps.base.viewsets import CustomerModelViewSet

from datamodels.common.models import mm_AppVersion
from apps.customer.common.serializers import AppVersionSerializer


class CustomerAppVersionViewSet(CustomerModelViewSet):

    queryset = mm_AppVersion.published_versions()
    serializer_class = AppVersionSerializer


    @action(detail=False,)
    def latest_ios(self, request):
        version = mm_AppVersion.get_latest_version(mm_AppVersion.OS_TYPE_IOS)
        if version:
            data = self.serializer_class(version).data
        else:
            data = {}
        return Response(data=data)

    @action(detail=False,)
    def latest_android(self, request):
        version = mm_AppVersion.get_latest_version(mm_AppVersion.OS_TYPE_ANDROID)
        if version:
            data = self.serializer_class(version).data
        else:
            data = {}
        return Response(data=data)





