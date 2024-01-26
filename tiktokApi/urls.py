from django.urls import path
from rest_framework import routers
from .views import VideoViewSet, ParticipantViewSet, SessionViewSet, DataFileUpload

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video_list')
router.register(r'participant', ParticipantViewSet, basename='participants')
router.register(r'session', SessionViewSet, basename='video_list')
urlpatterns = router.urls

urlpatterns += [
    path('save/data-upload/', DataFileUpload.as_view(), name='video-data-csv'),

]