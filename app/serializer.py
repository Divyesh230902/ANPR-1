from rest_framework import serializers
from .models import image_storage

class image_serializer(serializers.ModelSerializer):
    class Meta:
        model = image_storage
        fields = '__all__'