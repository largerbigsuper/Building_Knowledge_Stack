from rest_framework import serializers

class SMSSerializer(serializers.Serializer):

    account = serializers.CharField()

