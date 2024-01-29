from django.db import models
from django.utils import timezone
import uuid

class RegionInfo(models.Model):
    region_code = models.CharField(primary_key=True, max_length=5)
    region_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'region_info'

class VideoInfo(models.Model):
    video_id = models.CharField(max_length=50, primary_key=True)
    description = models.TextField()
    user_name = models.CharField(max_length=50)
    region_code = models.ForeignKey(RegionInfo, db_column="region_code", on_delete= models.CASCADE)
    create_time = models.DateTimeField(blank=True, null=True)
    music_id = models.CharField(max_length=50, blank=True, null=True)
    duration = models.BigIntegerField()

    class Meta:
        db_table = 'video_info'
        
    def __str__(self):
        return f"videoId: {self.video_id}\n description: {self.description}\n createdUser: {self.user_name}\n videoDuration: {self.duration}"

class HashtagInfo(models.Model):
    hashtag_id = models.BigAutoField(primary_key=True)
    hashtag_name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        db_table = 'hashtag_info'
    
    def __str__(self):
        return f"HashtagId: {self.hashtag_id}\n Name: {self.hashtag_name}"

class VideoHashtagMap(models.Model):
    uniq_id = models.AutoField(primary_key=True)
    video_id = models.ForeignKey(VideoInfo, db_column="video_id", on_delete=models.CASCADE)
    hashtag_id = models.ForeignKey(HashtagInfo, db_column="hashtag_id", on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'video_hashtag_map'
        unique_together = ('video_id', 'hashtag_id')

class AuthInfo(models.Model):
    auth_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    access_key = models.IntegerField(unique=True)
    
    class Meta:
        db_table = 'auth_info'

class SessionInfo(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth_id = models.ForeignKey(AuthInfo, db_column="auth_id", on_delete= models.CASCADE)
    experiment_condition = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now())
    end_time = models.DateTimeField(default=lambda: timezone.now() + timezone.timedelta(minutes=30))

    class Meta:
        db_table = 'session_info'

    def __str__(self):
        return f"SessionID: {self.session_id}\n authId: {self.auth_id}\n experiment: {self.experiment_condition}"


class ParticipantInteractions(models.Model):
    watch_id = models.IntegerField(primary_key=True)
    session_id = models.ForeignKey(SessionInfo, db_column="session_id", on_delete= models.CASCADE)
    video_id = models.ForeignKey(VideoInfo, db_column="video_id", on_delete= models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(default=lambda: timezone.now() + timezone.timedelta(minutes=30))
    is_liked = models.BooleanField(null=True)

    class Meta:
        db_table = 'participant_interactions'

class Comments(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    comment_text = models.TextField(null=True)
    video_id = models.ForeignKey(VideoInfo, db_column="video_id", on_delete= models.CASCADE)
    parent_comment_id = models.BigIntegerField(null=True)
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    comment_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'comment_info'

class VideoInteractions(models.Model):
    video_id = models.ForeignKey(VideoInfo, db_column="video_id", on_delete= models.CASCADE, primary_key=True)
    like_count = models.IntegerField(default=0, null=True)
    view_count = models.IntegerField(default=0, null=True)
    share_count = models.IntegerField(default=0, null=True)
    comment_count = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'video_interaction'
