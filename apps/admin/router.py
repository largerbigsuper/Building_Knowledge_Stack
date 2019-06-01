from rest_framework import routers

from apps.admin.subjects.viewsets import AdminSubjectViewSet, AdminSubjectTermViewSet


admin_router = routers.DefaultRouter()

admin_router.register('subject', AdminSubjectViewSet,
                      base_name='admin-subject')
admin_router.register('subject-term', AdminSubjectTermViewSet,
                      base_name='admin-subject-term')
