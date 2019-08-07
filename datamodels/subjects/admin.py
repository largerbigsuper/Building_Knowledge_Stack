from django.contrib import admin, messages

from datamodels.subjects.models import Subject, SubjectTerm, Application, SubjectConfig

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(SubjectTerm)
class SubjectTermAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    
    fields = ['id', 'customer', 'name', 'tel', 'id_number', 'total_amount', 'subject_term', 'pay_at', 'status', 'union_trade_no']


@admin.register(SubjectConfig)
class SubjectConfigAdmin(admin.ModelAdmin):
    
    # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    #     """只返回以及科目"""
    #     if db_field.name == 'subject':
    #         kwargs["queryset"] = Subject.objects.filter(level=0)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not all([obj.danxuan_count, obj.duoxuan_count, obj.panduan_count]):
            return messages.error(request, '未设置考试题目个数')
            
        return super().save_model(request, obj, form, change)

