# 初始化tags

from django.conf import settings

from datamodels.articles.models import mm_Tag

def run():
    for pk, name in mm_Tag.Tag_Choice:
        # print(name)
        tag, created = mm_Tag.get_or_create(pk=pk, defaults={'name':name})
        tag.name = name
        tag.save()
        
