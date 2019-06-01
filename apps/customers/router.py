from rest_framework import routers

from apps.customers.customers.viewsets import CustomerViewSet


customer_router = routers.DefaultRouter()

customer_router.register('u', CustomerViewSet, base_name='customer')
