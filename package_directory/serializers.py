from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.Serializer):
    
    package_name = serializers.CharField(required=False, allow_blank=True, max_length=42)
    package_version_code = serializers.CharField(required=False, allow_blank=True, max_length=10)
    application = serializers.FileField(source='apk_file', max_length=None, allow_empty_file=False, use_url=True)


class ApplicationSerializerUpload(serializers.ModelSerializer):
    
    application = serializers.FileField(source='apk_file', max_length=None, allow_empty_file=False, use_url=True)
    
    class Meta:
        model = Application
        fields = ['description', 'application']
