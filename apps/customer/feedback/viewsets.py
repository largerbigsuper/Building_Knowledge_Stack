from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from datamodels.feedback.models import mm_Feedback
from apps.customer.feedback.serializers import CustomerFeedbackSerilizer


class CustomerFeedbackViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated] 
    serializer_class = CustomerFeedbackSerilizer       

    def get_queryset(self):
        return mm_Feedback.filter(customer_id=self.request.user.customer.id)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)
    
