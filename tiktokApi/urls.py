from django.urls import path
from . import views

urlpatterns = [
    path('videos', views.list_videos),
    path('data', views.videos_data)
]