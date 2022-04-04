from django.shortcuts import redirect, render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import json
import random
import requests

class Search(GenericAPIView):
    def get(self,request):
        return render(request,'search.html')
    def post(self,request):
        genre = request.POST.get('searchBox')
        redirect_url = 'tracks/' + genre
        return redirect(redirect_url)


class TrackInfo(GenericAPIView):
    #Get tour informations
    def get(self,request,genre):
        with open('genres.json','r') as f:
            genres_list = json.load(f)
        
        arts = []
        names = []
        images = []
        links = []
        try:
            artist_arr = genres_list[genre]
            random_artist = random.choice(artist_arr)
            data = {"grant_type":"client_credentials","redirect_uri":"http://127.0.0.1:8000","code":'null'}
            token_response = requests.post(data=data, url="https://accounts.spotify.com/api/token",headers={"Content-Type": "application/x-www-form-urlencoded","Authorization": "Basic Y2NiOGI5YWJjOTlmNDUyNjg5ZTkxY2Y1NmIxODYyYzg6ZmFmOTM3NGEyYTI5NGMyMDgyZTI2MDlkOGFhZTY2NDk="})
            access_token = json.loads(token_response.content.decode())['access_token']
            url_query = 'https://api.spotify.com/v1/search?q='+random_artist + '&type=track&limit=10'
            authorization = 'Bearer ' + access_token
            info_response = requests.get(url=url_query,headers={"Authorization":authorization,"Content-Type":"application/json"})
            json_response = json.loads(info_response.content.decode())
            
            items = json_response["tracks"]["items"]
            for i in items:
                if i["artists"]:
                    arts.append(i["artists"][0]["name"])
                    links.append(i["external_urls"]["spotify"])
                if i["name"]:
                    names.append(i["name"])
                if i["album"]["images"]:
                    images.append(i["album"]["images"][0]["url"])
            
        except Exception as e:
            print(e)
            return render(request,'list.html',{'arts':arts,'names':names,'images':images ,'links':links})

        #return Response(json_response,status=200)
        return render(request,'list.html',{'arts':arts,'names':names,'images':images,'links':links})

        