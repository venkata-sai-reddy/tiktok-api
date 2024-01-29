from django.shortcuts import render
from json import JSONDecodeError
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import action
import requests
from rest_framework import viewsets, status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.views import APIView, View
from .models import VideoInfo, RegionInfo, HashtagInfo, VideoHashtagMap, ParticipantInteractions, SessionInfo, AuthInfo, VideoInteractions
import pandas as pd
from .serializers import VideoSerializer, VideoHashtagMapSerializer, ParticipantSerializer, SessionSerializer, AuthSerializer
from rest_framework.parsers import JSONParser
from .forms import YourModelForm, GenerateAccessKeyForm
import csv
import re
import random
import string
import pandas as pd
from .exceptions import TiktokException
from .utils import validate_participant_interactions, check_is_session_exists, current_time, unix_to_datetime

class VideoViewSet (ListModelMixin,
        RetrieveModelMixin,
        viewsets.GenericViewSet) :
    """
    A simple viewset for listing, reteiving and saving Video data
    """
    serializer_class = VideoSerializer

    @action(detail=False, methods=['POST'], url_path='hashtag')
    def get_by_hashtag(self, request):
        try:
            data = JSONParser().parse(request)
            hashtags = data.get('hashtags')
            hashtagIds  = [ids for ids, in HashtagInfo.objects.filter(hashtag_name__in = hashtags).values_list("hashtag_id")]
            videoIds = [ids for ids, in VideoHashtagMap.objects.filter(hashtag_id__in = hashtagIds).values_list("video_id")]
            videos = VideoInfo.objects.filter(video_id__in = videoIds)
            serializer = VideoSerializer(videos, many=True)
            return Response(serializer.data)
        except Exception as e :
            return JsonResponse({"result": "error", "message": str(e)}, status=400)
    
    def get_queryset(self):
        try:
            return VideoInfo.objects.all()
        except JSONDecodeError:
            return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)

class ParticipantViewSet (
        CreateModelMixin,
        viewsets.GenericViewSet) :
    """
    A simple viewset for saving Participants Interactions
    """
    serializer_class = ParticipantSerializer

    @action(detail=False, methods=['POST'], url_path='save')
    def save_participant_interactions(self, request):
        try:
            data = JSONParser().parse(request)
            validate_participant_interactions(data)
            video_data = VideoInfo.objects.get(video_id = "'"+data.get('video_id')+"'")
            session_data = SessionInfo.objects.get(session_id = data.get('session_id'))
            participant_interaction = ParticipantInteractions.objects.create(video_id = video_data, session_id = session_data, start_time = data.get('start_time'),
                end_time = data.get('end_time'), is_liked = bool(data.get('is_liked')))
            participant_interaction = ParticipantInteractions.objects.get(video_id = video_data, session_id = session_data, start_time = data.get('start_time'),
                end_time = data.get('end_time'), is_liked = bool(data.get('is_liked')))
            serializer = ParticipantSerializer(participant_interaction)
            return Response(serializer.data)
        except VideoInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Unable to Find Video"}, status = 400)
        except SessionInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Session Not Exists"}, status = 401)
        except Exception as e :
            return JsonResponse({"result": "error", "message": str(e)}, status=400)

class SessionViewSet (RetrieveModelMixin,
        CreateModelMixin,
        viewsets.GenericViewSet) :
    """
    A simple viewset for Retrieving, Updating and Saving Session Information
    """
    serializer_class = SessionSerializer

    @action(detail=False, methods=['POST'], url_path='start')
    def create_session_information(self, request):
        try:
            data = JSONParser().parse(request)
            if 'access_key' in data:
                auth_data = AuthInfo.objects.get(access_key = data.get('access_key'))
                session_data = ()
                if 'experiment_condition' in data:
                    session_data = SessionInfo.objects.get_or_create(
                        auth_id = auth_data,
                        experiment_condition = data.get('experiment_condition')
                    )
                    check_is_session_exists(session_data)
                    return Response(SessionSerializer(SessionInfo.objects.get(auth_id = auth_data, experiment_condition = data.get('experiment_condition'))).data)
                else:
                    session_data = SessionInfo.objects.get_or_create(
                        auth_id = auth_data,
                        experiment_condition = 1
                    )
                    check_is_session_exists(session_data)
                    return Response(SessionSerializer(SessionInfo.objects.get(auth_id = auth_data, experiment_condition = 1)).data)
            else:
                raise TiktokException("Access Key Required")
        except AuthInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Unauthorized to access"}, status = 401)
        except SessionInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Session Not Exists"}, status = 401)
        except Exception as e :
            return JsonResponse({"result": "error", "message": str(e)}, status=400)

    @action(detail=False, methods=['POST'], url_path='create')
    def save_session_information(self, request):
        try:
            data = JSONParser().parse(request)
            if 'session_id' in data and 'experiment_condition' in data:
                session_info = SessionInfo.objects.get(session_id=data.get('session_id'))
                auth_data = AuthInfo.objects.get(auth_id = session_info.auth_id.auth_id)
                session_data = SessionInfo.objects.get_or_create(
                    auth_id = auth_data,
                    experiment_condition = data.get('experiment_condition')
                )
                check_is_session_exists(session_data)
                return Response(SessionSerializer(SessionInfo.objects.get(auth_id = auth_data,
                    experiment_condition = data.get('experiment_condition'))).data)
            else :
                raise TiktokException("Data field are Required")
        except AuthInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Unauthorized to access"}, status = 401)
        except SessionInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Session Not Exists"}, status = 401)
        except Exception as e :
            return JsonResponse({"result": "error", "message": str(e)}, status=400)
    
    @action(detail=False, methods=['PUT'], url_path='save')
    def close_session_information(self, request):
        try:
            data = JSONParser().parse(request)
            if 'session_id' in data and 'experiment_condition' in data:
                session_info = SessionInfo.objects.get(session_id=data.get('session_id'))
                auth_data = AuthInfo.objects.get(auth_id = session_info.auth_id.auth_id)
                SessionInfo.objects.filter(session_id = session_info.session_id).update(end_time = current_time())
                return Response(SessionSerializer(SessionInfo.objects.get( session_id = session_info.session_id)).data)
            else :
                raise TiktokException("Data field are Required")
        except AuthInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Unauthorized to access"}, status = 401)
        except SessionInfo.DoesNotExist as e:
            return JsonResponse({"result": "error", "message": "Session Not Exists"}, status = 401)
        except Exception as e :
            return JsonResponse({"result": "error", "message": str(e)}, status=400)

class DataFileUpload(View):
    template_name = 'manage-data.html'

    def get(self, request):
        form = YourModelForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = YourModelForm(request.POST, request.FILES)

        # Check if the form is valid
        if form.is_valid():
            csv_file = request.FILES['file_name']
            # Process CSV file and save data to the database
            try:
                video_data = pd.read_csv(csv_file)
                video_data.dropna(subset=['id', 'video_description', 'username', 'region_code', 'create_time', 'music_id', 'search_key',
                 'like_count', 'view_count', 'share_count', 'comment_count'], inplace=True)
                video_data = video_data[video_data['music_id'].notna() & (video_data['music_id'] != '') & (video_data['music_id'] != 'None')]

                for index, data in video_data.iterrows():
                    region_info = RegionInfo.objects.get(region_code=data['region_code'])
                    video_duration = data['duration'] if 'duration' in data else 60
                    # Insert data into VideoInfo
                    video_info, created = VideoInfo.objects.get_or_create(
                        video_id=data['id'],
                        defaults={
                            'description': data['video_description'],
                            'user_name': data['username'],
                            'region_code': region_info,
                            'create_time': unix_to_datetime(data['create_time']),
                            'music_id': data['music_id'],
                            'duration': video_duration
                        }
                    )
                    # Fetching the video_info data instance from the database
                    video_info = VideoInfo.objects.get(video_id=data['id'])
                    # Saving the Hashtag information
                    hashtag_name = re.search(r'hashtag_name\s+([^ ]+)', data['search_key']).group(1)
                    hashtag_info, created = HashtagInfo.objects.get_or_create(hashtag_name=hashtag_name)
                    # Fetching the Hashtag instance data fromt he database
                    hashtag_info = HashtagInfo.objects.get(hashtag_name=hashtag_name)
                    # Saving the Video Hashtag mapping into the databse if not exists
                    if VideoHashtagMap.objects.filter(video_id=video_info, hashtag_id=hashtag_info).count() == 0:
                        VideoHashtagMap.objects.create(video_id=video_info, hashtag_id=hashtag_info)
                    
                    # Insert data into VideoInteractions if not exists
                    if VideoInteractions.objects.filter(video_id = video_info).count() == 0:
                        VideoInteractions.objects.create(
                            video_id=video_info,
                            like_count = data['like_count'],
                            view_count= data['view_count'],
                            share_count= data['share_count'],
                            comment_count= data['comment_count']
                        )
                    
                return render(request, self.template_name, {'form': form, 'status': 'success', 'message': 'CSV file uploaded successfully!'})
                # return JsonResponse({'status': 'success', 'message': 'CSV file uploaded successfully!'})
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'status': 'error', 'message': str(e)})
                # return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            if 'delete_all' in request.POST:
                try:
                    # Delete all records
                    VideoHashtagMap.objects.all().delete()
                    VideoInteractions.objects.all().delete()
                    HashtagInfo.objects.all().delete()
                    VideoInfo.objects.all().delete()
                    return render(request, self.template_name, {'form': form, 'status': 'success', 'message': 'All records deleted successfully!'})
                    # return JsonResponse({'status': 'error', 'message': 'All records deleted successfully!'})
                except Exception as e:
                    return render(request, self.template_name, {'form': form, 'status': 'error', 'message': str(e)})
                    # return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        return render(request, self.template_name, {'form': form, 'status': 'error', 'message': 'Invalid form submission'})


class GeneratedAccessKeyView(View):
    model = AuthInfo
    template_name = 'generate_access_key.html'
    context_object_name = 'generated_keys'
    form_class = GenerateAccessKeyForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = GenerateAccessKeyForm(request.POST)
        try:
            if form.is_valid():
                n = form.cleaned_data['n']
                unique_keys = set()

                while len(unique_keys) < n:
                    new_key = self.generate_unique_key(6)
                    if int(new_key) > 100000 and new_key not in unique_keys and not AuthInfo.objects.filter(access_key=new_key).exists():
                        unique_keys.add(new_key)
                        AuthInfo.objects.create(access_key=new_key)
            return render(request, self.template_name, {'form': form, 'status': 'success', 'generated_keys': unique_keys})
        except Exception as e:
            return render(request, self.template_name, {'form': form, 'status': 'error', 'message': str(e)})

    @staticmethod
    def generate_unique_key(length):
        return ''.join(random.choices(string.digits, k=length))
