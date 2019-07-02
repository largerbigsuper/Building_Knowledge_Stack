from django_filters import rest_framework as filters

from datamodels.articles.models import Article


class ArticleFliter(filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'tags': ['exact']
        }