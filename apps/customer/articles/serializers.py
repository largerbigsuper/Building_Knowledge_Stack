from rest_framework import serializers

from datamodels.articles.models import mm_Tag, mm_Article


class CustomerTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = mm_Tag.model
        fields = ['id', 'name']



class CustomerArticleSerializer(serializers.ModelSerializer):
    
    tags = CustomerTagSerializer(many=True)

    class Meta:
        model = mm_Article.model
        fields = ['id', 'headline', 'image', 'content', 'create_at', 'update_at', 'tags']