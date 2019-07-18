from rest_framework import serializers

from datamodels.customers.models import Customer

Profile_Fields = ('id', 'user_id', 'account', 'name', 'age',
                  'gender', 'avatar_url', 'create_at', 'invite_code')


class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()


class RegisterSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField(max_length=4)
    invite_code = serializers.CharField(max_length=4, required=False)


class LoginSerializer(serializers.Serializer):

    account = serializers.CharField()
    password = serializers.CharField()


class PasswordSerializer(serializers.ModelSerializer):

    account = serializers.CharField()
    password = serializers.CharField()
    code = serializers.CharField()

    class Meta:
        model = Customer
        fields = ['account', 'password', 'code']


class CustomerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = Profile_Fields
        read_only_fields = ('user_id', 'account', 'invite_code')
