from django.urls import path
from . import views

urlpatterns = [
    path('api/videos/', views.get_video_info, name='video-list'),
    path('save/hashtags', views.save_hashtags, name='upload_hashtags'),
    # path('save/hashtags_map', views.save_hashtags_map, name='update_hashtag_map'),
    path('save/upload-csv/', views.UploadCSV.as_view(), name='upload-hashtag-map-csv')
]