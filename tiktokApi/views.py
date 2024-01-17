from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers
import requests
from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VideoInfo, HashtagInfo
import pandas as pd


"""
Connect to Oembed tiktok API to fetch the blockquote for UI
"""
def get_oembed_html(request, video_info):
    api_url = "https://www.tiktok.com/oembed"
    params = {
        'url': f"https://www.tiktok.com/@{video_info['user_name']}/video/{video_info['video_id']}"
    }
    try:
        print(params['url'])
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


"""
Create an Video object to send to the UI 
If the Oembed Fails then create an custom blockquote
"""
def create_video_info_dict(video_info, embed_data):
    return {
        'video_id': video_info['video_id'],
        'description': video_info['description'],
        'user_name': video_info['user_name'],
        'region_code': video_info['region_code'],
        'create_time': video_info['create_time'],
        'music_id': video_info['music_id'],
        'duration': video_info['duration'],
        'html': embed_data['html'] if embed_data else f"<blockquote class=\"tiktok-embed\" cite=\"https://www.tiktok.com/@{video_info['user_name']}/video/{video_info['video_id']}\" data-video-id=\"{video_info['video_id']}\" data-embed-from=\"oembed\" style=\"max-width: 605px;min-width: 325px;\" > <section> <a target=\"_blank\" title=\"@{video_info['user_name']}\" href=\"https://www.tiktok.com/@{video_info['user_name']}?refer=embed\">@{video_info['user_name']}</a> <p>{video_info['description']}</p> <a target=\"_blank\" title=\" original sound - {video_info['user_name']}\" href=\"https://www.tiktok.com/music/original-sound-{video_info['music_id']}?refer=embed\"> original sound - {video_info['user_name']}</a> </section> </blockquote>",  
    }

"""
Retrieve All the Video Information from the database
"""
def get_video_info(request):
    video_info_objects = VideoInfo.objects.values()[:2]
    video_info_data = []

    for video_info in video_info_objects:
        # Retrieve blockquote from oembed
        embed_data = get_oembed_html(request, video_info)
        video_info_data.append(create_video_info_dict(video_info, embed_data))

    return JsonResponse(video_info_data, safe=False)  

"""
Retrieve All the Video Information from the database
"""
def save_hashtags(request):
    
    hashtags_data = ["adventure", "alt", "balloonartist", "balloondecor", "basketball", "bookish", "bookrecommendations", "bookworm", "bouquet", "camping", "candle", "case", "catlover", "catsoftiktok", "chef", "chevy", "christmas2023", "christmasdecor", "christmasgift", "christmaslights", "christmasphotoshoot", "christmastiktok", "christmastree", "clearaligners", "cod", "cold", "construction", "coquette", "cup", "dadsoftiktok", "dentalimplants", "drone", "elf", "enhypen", "familytime", "foodreview", "ford", "forex", "forexlifestyle", "forextrading", "fortniteclips", "gift", "giftwrapping", "gingerbreadhouse", "grandparents", "grinch", "headphones", "hockey", "holiday", "holidays", "invisalign", "jjk", "journalwithme", "jujutsukaisen", "kanyewesr", "lashes", "laskeyesurgery", "lyrics", "mealprep", "miami", "mining", "momof1", "multivitamin", "mustang", "nailtech", "naturalhair", "nba", "ocean", "partyideas", "petsoftiktok", "phonecase", "pink", "planner", "porsche", "puppy", "ramobuchon", "reading", "restaurant", "santababy", "Shopping", "stanley", "stanleycup", "stationary", "sturniolotriplets", "taxes", "technology", "timeflies", "Toddlertok", "trucktok", "warzone"]

    for hashtag_name in hashtags_data:
        hashtag = HashtagInfo.objects.create(hashtag_name = hashtag_name)

    return JsonResponse(True, safe=False)  

class UploadCSV(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.data:
            return Response({'error': 'No file provided'}, status=400)
        
        file = request.FILES.get('file')
        csv_file = request.data['file']
        df = pd.read_csv(csv_file)

        # YourModel.objects.bulk_create(
        #     [YourModel(**row) for row in df.to_dict(orient='records')]
        # )

        return Response({'message': 'CSV data uploaded successfully'})
