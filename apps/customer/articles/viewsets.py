from rest_framework import viewsets
from rest_framework.decorators import action

from apps.customer.articles.serializers import CustomerArticleSerializer, CustomerTagSerializer, CustomerExamNoticeSerializer
from apps.base.viewsets import CustomerReadOnlyModelViewSet
from apps.customer.articles.filters import ArticleFliter, ExamNoticeFliter
from datamodels.articles.models import mm_Tag, mm_Article, mm_ExamNotice


class CustomerTagViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerTagSerializer
    queryset = mm_Tag.all()


class CustomerArticleViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerArticleSerializer
    queryset = mm_Article.published()
    filter_class = ArticleFliter


class CustomerExamNoticeViewSet(CustomerReadOnlyModelViewSet):

    serializer_class = CustomerExamNoticeSerializer
    queryset = mm_ExamNotice.published()
    filter_class = ExamNoticeFliter

