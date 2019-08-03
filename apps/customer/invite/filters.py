from django_filters import rest_framework as filters

from datamodels.invite.models import mm_InviteRecord

class CustomerInfiteFilter(filters.FilterSet):

    class Meta:
        model = mm_InviteRecord.model
        fields = {
            'action_type': ['exact'],
        }
