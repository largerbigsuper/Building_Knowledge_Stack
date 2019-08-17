from django.forms import ModelForm
from django.contrib.auth.models import User

from datamodels.customers.models import Customer


class CustomerForm(ModelForm):

    class Meta:
        model = Customer
        exclude = ['user']
    
    def save(self, commit=True):
        obj = super().save(commit=False)
        user, created = User.objects.get_or_create(username=obj.account)
        if created:
            user.set_password('888888')
            user.save()
        obj.user = user 
        obj.save()
        return obj
