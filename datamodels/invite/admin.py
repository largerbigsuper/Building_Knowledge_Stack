from django.contrib import admin, messages

from datamodels.invite.models import WithDrawRecord, mm_BlanceRecord, InviteRecord


@admin.register(InviteRecord)
class InviteRecordAdmin(admin.ModelAdmin):
    
    list_display = [f.name for f in InviteRecord._meta.fields]

@admin.register(WithDrawRecord)
class WithDrawRecordAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('customer', 'status', 'amount', 'operator')
    list_filter = ('status',)
    search_fields = ('customer__acount',)

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if form.initial['status'] == 0:
                if form.cleaned_data['status'] == 1:
                    # 扣除余额
                    total_point = mm_BlanceRecord.get_blance(obj.customer.id)
                    if obj.amount > total_point:
                        messages.error(request, '余额不足')
                        return
                    else:
                        mm_BlanceRecord.add_record(
                            customer_id=obj.customer.id,
                            amount=obj.amount,
                            action_type=mm_BlanceRecord.Action_Blance_Out,
                        )

        super(WithDrawRecordAdmin, self).save_model(request, obj, form, change)
