from django_filters import rest_framework as filters

from datamodels.articles.models import Article, ExamNotice


class ArticleFliter(filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'tags': ['exact']
        }


class ExamNoticeFliter(filters.FilterSet):

    class Meta:
        model = ExamNotice
        fields = {
            'subject': ['exact']
        }
