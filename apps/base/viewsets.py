from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class AdminModelViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAdminUser, IsAuthenticated]


class CustomerModelViewSet(viewsets.ModelViewSet):
    permission_classes = []


class CustomerReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pass