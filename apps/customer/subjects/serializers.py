from apps.base.serializers.subjects import BaseSubjectTermSerializer
from datamodels.subjects.models import mm_SubjectTerm


class CustomerSubjectTermSerializer(BaseSubjectTermSerializer):

    class Meta:
        model = mm_SubjectTerm.model
        fields = ['id', 'subject', 'name', 'price', 'price_info', 'subject_info',
                  'status', 'update_at', 'create_at']
