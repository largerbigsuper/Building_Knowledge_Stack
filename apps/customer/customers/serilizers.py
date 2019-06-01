from rest_framework import serializers

from datamodels.customers.models import Customer

Profile_Fields = ('id', 'user_id', 'account', 'name', 'age', 'gender', 'avatar_url', 'create_at')



class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()


class RegisterSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = Profile_Fields
        read_only_fields = ('user_id', 'account')



