from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.customer.router import customer_router
from apps.admin.router import admin_router

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('customer/', include(customer_router.urls)),
    path('staff/', include(admin_router.urls)),
]

urls = [
    # path('qiniutoken/', UploadTokenView.as_view()),
]

urlpatterns += urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = '浙江建筑培训'
admin.site.site_title = '浙江建筑培训'