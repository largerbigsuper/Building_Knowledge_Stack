from django.contrib import admin
from django.contrib.auth.models import User, Group

from rest_framework.authtoken.models import Token

from datamodels.customers.models import Customer
from datamodels.customers.forms import CustomerForm


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Token)


def set_inviter(modeladmin, request, queryset):
    for customer in queryset:
        customer.set_invite_code()

set_inviter.short_description = "设置为推广员"

def unset_inviter(modeladmin, request, queryset):
    queryset.update(invite_code=None)

unset_inviter.short_description = "取消推广员"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display  = [f.name for f in Customer._meta.fields]
    actions = [set_inviter, unset_inviter]
    form = CustomerForm
