from rest_framework import serializers

from datamodels.customers.models import Customer


class CustomerForeginKeySerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'name', 'age', 'gender', 'avatar_url']

