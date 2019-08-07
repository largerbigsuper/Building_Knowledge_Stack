# 初始化报名项目

from django.conf import settings

from datamodels.subjects.models import mm_Subject, mm_SubjectConfig, mm_SubjectTerm, mm_Application
from datamodels.questions.models import mm_Question, mm_QuestionRecord, mm_Exam
from datamodels.articles.models import mm_ExamNotice


GROUP_MAPPING = [
    {
        'name': '技工证',
        'child': [
                    {
                        'name': '砌筑工',

                    },
                    {
                        'name': '瓦工',

                    },
                    {
                        'name': '钢筋工',

                    },
                    {
                        'name': '架子工',

                    },
                    {
                        'name': '混凝土工',

                    },
                    {
                        'name': '模板工',

                    },
                    {
                        'name': '防水工',

                    },
                    {
                        'name': '木工',

                    },
                    {
                        'name': '测量工',

                    },

                    {
                        'name': '机械设备安装工',

                    },
                    {
                        'name': '通风工',

                    },
                    {
                        'name': '焊工',

                    },
                    {
                        'name': '电气安装调试工',

                    },
                    {
                        'name': '电工管道工',

                    },
                    {
                        'name': '起重信号司索工',

                    },
                    {
                        'name': '建筑起重机械安装拆卸工',

                    },
                    {
                        'name': '起重工',

                    },
                    {
                        'name': '抹灰工',
                    },
                    {
                        'name': '镶贴工',
                    },
                    {
                        'name': '油漆工',
                    },
                    {
                        'name': '石作业工',
                    },
                    {
                        'name': '水电工',
                    },
                    {
                        'name': '除尘工',
                    },
                    {
                        'name': '泥塑工',
                    },
                    {
                        'name': '砧细工',
                    },
                    {
                        'name': '彩绘工',
                    },
                    {
                        'name': '匾额工',
                    },
                    {
                        'name': '推光漆工',
                    },
                    {
                        'name': '砌花街工',
                    },
                    {
                        'name': '石雕工',
                    },
                    {
                        'name': '木雕工',
                    },
                    {
                        'name': '砧刻工',
                    },
                    {
                        'name': '下水道工',
                    },
                    {
                        'name': '下水道养护工',
                    },
                    {
                        'name': '道路养护工',
                    },
                    {
                        'name': '中小型机械操作工',
                    },
                    {
                        'name': '筑路工',
                    },
                    {
                        'name': '沥青工',
                    },
                    {
                        'name': '沥青混凝土摊铺机操作工',
                    },
                    {
                        'name': '绿化工',
                    },
                    {
                        'name': '花卉工',
                    },
                    {
                        'name': '假山工',
                    },
                    {
                        'name': '盆景工',
                    },
                    {
                        'name': '植保工',
                    },
                    {
                        'name': '草坪建值工',
                    }
                ]
    },
    {
        # 施工员 质量员 资料员 材料员 劳务员 机械员 标准员
        'name': '七大员',
        'child': [
            {
                'name': '施工员',
            },
            {
                'name': '质量员',
            },
            {
                'name': '资料员',
            },
            {
                'name': '材料员',
            },
            {
                'name': '劳务员',
            },
            {
                'name': '机械员',
            },
            {
                'name': '标准员',
            }
        ]
    },
    {
        # 建筑电工 建筑焊工 建筑普通脚手架架子工 建筑附着升降脚手架架子工 建筑起重信号司索工 建筑塔式起重机司机 建筑施工升降机司机 建筑物料提升机司机
        # 建筑塔式起重机安装拆卸工 建筑施工升降机安装拆卸工 建筑物料提升机安装拆卸工 高处作业吊篮安装拆卸工
        'name': '特种工',
        'child': [
            {
                'name': '建筑电工',
            },
            {
                'name': '建筑焊工',
            },
            {
                'name': '建筑普通脚手架架子工',
            },
            {
                'name': '建筑附着升降脚手架架子工',
            },
            {
                'name': '建筑起重信号司索工',
            },
            {
                'name': '建筑塔式起重机司机',
            },
            {
                'name': '建筑施工升降机司机',
            },
            {
                'name': '建筑物料提升机司机',
            },
            {
                'name': '建筑塔式起重机安装拆卸工',
            },
            {
                'name': '建筑施工升降机安装拆卸工',
            },
            {
                'name': '建筑物料提升机安装拆卸工',
            },
            {
                'name': '高处作业吊篮安装拆卸工',
            }

        ]
    },
    {
        # 企业主要负责人-A证 项目负责人-B证 专职安全员-C证
        'name': '三类人员',
        'child': [
            {
                'name': '企业主要负责人-A证',
            },
            {
                'name': '项目负责人-B证',
            },
            {
                'name': '专职安全员-C证',
            }
        ]
    },
    {
        # 二级建造师继续教育 七大员继续教育 三类人员继续教育 特种工继续教育
        'name': '继续教育',
        'child': [
            {
                'name': '二级建造师继续教育',
            },
            {
                'name': '七大员继续教育',
            },
            {
                'name': '三类人员继续教育',
            },
            {
                'name': '特种工继续教育',
            }
        ]
    },
    {
        # 零基本升中专 零基础升大专 大专升本科
        'name': '学历提升',
        'child': [
            {
                'name': '零基本升中专',
            },
            {
                'name': '零基础升大专',
            },
            {
                'name': '大专升本科'
            }
        ]
    }

]

def print_excute_time(func):

    def inner(*args, **kwargs):
        print('{func_name} start...'.format(func_name=func.__name__))
        func(*args, **kwargs)
        print('{func_name} end.'.format(func_name=func.__name__))
    
    return inner


@print_excute_time
def truncate_table(table):
    sql = 'DELETE FROM {table};'.format(table=table) 
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)


@print_excute_time
def migrate_db():
    for item in GROUP_MAPPING:
        parent, _ = mm_Subject.get_or_create(name=item['name'])
        sub_group = item['child']
        for sub_item in sub_group:
            sub_parant, _ = mm_Subject.get_or_create(name=sub_item['name'], parent=parent)
            for sub_item_3 in sub_item.get('child', []):
                result, _ = mm_Subject.get_or_create(name=sub_item_3['name'], parent=sub_parant)


def run():
    truncate_table(mm_SubjectConfig.model._meta.db_table)
    truncate_table(mm_ExamNotice.model._meta.db_table)
    truncate_table(mm_Exam.model._meta.db_table)
    truncate_table(mm_Application.model._meta.db_table)
    truncate_table(mm_SubjectTerm.model._meta.db_table)
    truncate_table(mm_QuestionRecord.model._meta.db_table)
    truncate_table(mm_Question.model._meta.db_table)
    truncate_table(mm_Subject.model._meta.db_table)
    migrate_db()
