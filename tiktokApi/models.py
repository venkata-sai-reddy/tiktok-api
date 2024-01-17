from django.db import models

class RegionInfo(models.Model):
    region_code = models.CharField(primary_key=True, max_length=5)
    region_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'region_info'

class VideoInfo(models.Model):
    video_id = models.BigIntegerField(primary_key=True)
    description = models.TextField()
    user_name = models.CharField(max_length=50)
    region_code = models.ForeignKey(RegionInfo, to_field="region_code", on_delete= models.CASCADE)
    create_time = models.DateTimeField(blank=True, null=True)
    music_id = models.BigIntegerField(blank=True, null=True)
    duration = models.BigIntegerField()

    class Meta:
        db_table = 'video_info'
        
    def __str__(self):
        return f"videoId: {self.video_id}\n description: {self.description}\n createdUser: {self.user_name}\n videoDuration: {self.duration}"

class HashtagInfo(models.Model):
    hashtag_id = models.BigIntegerField(primary_key=True)
    hashtag_name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        db_table = 'hashtag_info'

class VideoHashtagMap(models.Model):
    video_id = models.BigIntegerField()
    hashtag_id = models.BigIntegerField()

    class Meta:
        db_table = 'video_hashtag_map'
        
class SessionInfo(models.Model):
    session_id = models.BigIntegerField(primary_key=True)
    access_key = models.IntegerField()
    experiment_condition = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'session_info'
    
class ParticipantInteractions(models.Model):
    watch_id = models.BigIntegerField(primary_key=True)
    session_id = models.BigIntegerField()
    video_id = models.BigIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_liked = models.BooleanField(null=True)

    class Meta:
        db_table = 'participant_interactions'

class Comments(models.Model):
    comment_id = models.BigAutoField(primary_key=True)
    comment_text = models.TextField(null=True)
    video_id = models.BigIntegerField()
    parent_comment_id = models.BigIntegerField(null=True)
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    comment_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'comment_info'

class VideoInteractions(models.Model):
    video_id = models.BigAutoField(primary_key=True)
    like_count = models.IntegerField(default=0, null=True)
    view_count = models.IntegerField(default=0, null=True)
    share_count = models.IntegerField(default=0, null=True)
    comment_count = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = 'video_interaction'
