from rest_framework import serializers
from .models import VideoInfo

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInfo
        fields = '__all__'
