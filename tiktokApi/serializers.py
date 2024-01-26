from rest_framework import serializers
from .models import VideoInfo, HashtagInfo, VideoHashtagMap, ParticipantInteractions, SessionInfo, AuthInfo

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInfo
        fields = '__all__'

class HashtagInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashtagInfo
        fields = '__all__'

class VideoHashtagMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoHashtagMap
        fields = ['video_id', 'hashtag_id']
        exclude = ['id']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantInteractions
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionInfo
        fields = '__all__'

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthInfo
        fields = '__all__'