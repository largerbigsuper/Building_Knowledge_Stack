from rest_framework import viewsets

from apps.customer.articles.serializers import CustomerArticleSerializer, CustomerTagSerializer
from apps.base.viewsets import CustomerReadOnlyModelViewSet
from apps.customer.articles.filters import ArticleFliter
from datamodels.articles.models import mm_Tag, mm_Article


class CustomerTagViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerTagSerializer
    queryset = mm_Tag.all()


class CustomerArticleViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerArticleSerializer
    queryset = mm_Article.published()
    filter_class = ArticleFliter

