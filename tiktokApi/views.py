from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import serializers

videos = {"data" : [
    {
        "hashtag_names": [
            "model",
            "fashion",
            "luxury",
            "lamborghini",
            "fyp",
            "supermodel",
            "luxurylifestyle",
            "hermes",
            "luxurylife",
            "luxurygirl",
            "luxuryliving",
            "hermesbirkin",
            "hermeskelly",
            "luxurybag"
        ],
        "id": 7189033051341524270,
        "region_code": "US",
        "share_count": 0,
        "username": "luxurylife84",
        "comment_count": 0,
        "like_count": 9,
        "music_id": 7174260137358641966,
        "video_description": "Hermes Kelly #luxury #luxurylife #luxurylifestyle #luxurygirl #luxuryliving #supermodel #luxurybag #model #fashion #lamborghini #hermeskelly #hermes #hermesbirkin #fyp ",
        "view_count": 32,
        "create_time": 1673827199,
        "url":"https://www.tiktok.com/embed/7189033051341524270"
    },
    {
        "create_time": 1673827199,
        "hashtag_names": [],
        "like_count": 41,
        "music_id": 6956008818153114374,
        "share_count": 0,
        "video_description": "",
        "view_count": 2,
        "comment_count": 1,
        "region_code": "US",
        "username": "_that_camaro_15ls_",
        "id": 7189033042432806186,
        "url":"https://www.tiktok.com/embed/7189033042432806186"
    },
    {
        "comment_count": 3,
        "hashtag_names": [],
        "share_count": 0,
        "username": "nicmallars",
        "region_code": "US",
        "video_description": "I love you all fr ",
        "view_count": 5,
        "create_time": 1673827199,
        "id": 7189033041338076458,
        "like_count": 23,
        "music_id": 7189033046358625066,
        "url":"https://www.tiktok.com/embed/7189033041338076458"
    },
    {
        "view_count": 92,
        "comment_count": 12,
        "like_count": 41,
        "region_code": "US",
        "video_description": "#duet with @evankriel #newbeginnings it can be difficult to take that first step into public ministry, but when you do, a whole new world opens up.  #God #Jesus  #Christian #Bible #Love #inspirational ",
        "share_count": 1,
        "username": "zahamaru",
        "create_time": 1673827198,
        "hashtag_names": [
            "love",
            "god",
            "bible",
            "jesus",
            "inspirational",
            "duet",
            "christian",
            "newbeginnings"
        ],
        "id": 7189033041006890286,
        "music_id": 6786896889338923009,
        "url":"https://www.tiktok.com/embed/7189033041006890286"
    },
    {
        "like_count": 5,
        "music_id": 7189033026553236266,
        "region_code": "US",
        "view_count": 5,
        "comment_count": 1,
        "hashtag_names": [],
        "share_count": 0,
        "username": "timwiles961",
        "video_description": "live at hoots pub Amarillo 1/15/23. I do not own the rights to this song. ",
        "create_time": 1673827197,
        "id": 7189033041006759214,
        "url":"https://www.tiktok.com/embed/7189033041006759214"
    },
    {
        "comment_count": 0,
        "hashtag_names": [
            "plants",
            "plantlover",
            "plantsoftiktok",
            "micans",
            "planttok",
            "propegation",
            "propegationsong",
            "micanpropegation"
        ],
        "region_code": "US",
        "share_count": 0,
        "username": "houseplantingmama",
        "video_description": "Micans propagation.  #propegation #plantlover #micans #plants #planttok #plantsoftiktok #propegationsong #micanpropegation ",
        "view_count": 95,
        "create_time": 1673827199,
        "id": 7189033039643675946,
        "like_count": 65,
        "music_id": 6970430816019024646,
        "url":"https://www.tiktok.com/embed/7189033039643675946"
    }
]}

def list_videos(request):
    return render(request, 'videos.html', videos)

def videos_data(request):
    return JsonResponse(videos)