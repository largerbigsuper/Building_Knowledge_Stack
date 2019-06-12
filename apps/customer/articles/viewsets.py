from rest_framework import viewsets

from apps.customer.articles.serializers import CustomerArticleSerializer
from apps.base.viewsets import CustomerReadOnlyModelViewSet

from datamodels.articles.models import mm_Tag, mm_Article


class CustomerArticleViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerArticleSerializer
    queryset = mm_Article.published()

