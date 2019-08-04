from rest_framework import serializers

from datamodels.common.models import AppVersion


class AppVersionSerializer(serializers.ModelSerializer):

    os_type = serializers.SerializerMethodField()
    
    def get_os_type(seld, obj):
        return obj.get_os_type_display()


    class Meta:
        model = AppVersion
        fields = ['os_type', 'code', 'description']

