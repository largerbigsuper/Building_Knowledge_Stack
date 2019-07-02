from rest_framework import serializers

from datamodels.feedback.models import mm_Feedback


class CustomerFeedbackSerilizer(serializers.ModelSerializer):

    class Meta:
        model = mm_Feedback.model
        fields = ['id', 'content', 'create_at', 'status']
        read_only_fields = ['create_at', 'status']