# 将技工类整理为二级分类
from datamodels.subjects.models import mm_Subject


def run():

    name = '技工证'
    subject = mm_Subject.get(name=name, level=0)
    level_1_subjects = mm_Subject.filter(level=1, parent=subject)
    for p in level_1_subjects:
        print(p.name)
    level_2_subjects = mm_Subject.filter(level=2).update(parent=subject)
    level_1_subjects.delete()
    