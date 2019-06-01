from rest_framework import routers

from apps.customer.customers.viewsets import CustomerViewSet
from apps.customer.subjects.viewsets import CustomerSubjectViewSet, CustomerSubjectermViewSet


customer_router = routers.DefaultRouter()

customer_router.register('u', CustomerViewSet, base_name='customer')
customer_router.register('subject', CustomerSubjectViewSet, base_name='customer-subject')
customer_router.register('subject-term', CustomerSubjectermViewSet, base_name='customer-subject-term')
