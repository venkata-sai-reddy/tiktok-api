from django.db import models

# Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=100)
    share_count = models.IntegerField()
    video_description = models.TextField()
    view_count = models.BigIntegerField()
    region_code = models.CharField(max_length=10)
    username = models.CharField(max_length=50)
    comment_count = models.BigIntegerField()
    create_time = models.CharField(max_length=20)
    hashtag_names = models.TextField()
    like_count = models.BigIntegerField()
    music_id = models.CharField(max_length=100)
