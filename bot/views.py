from fileinput import filename
import imp
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests, json, yaml,sys
from django.core import serializers
from django.contrib.auth.models import User
# Create your views here.
# chat/views.py
from django.shortcuts import render

def index(request, room_name):
    roomName = room_name
    return render(request, 'bot.html',{'room_name':roomName})

def bot(request):
    return render(request, 'chatbot.html',{'room_name':request.user.id})

def bbott(request):
    # posts = User.objects.all()
    # post_list = serializers.serialize('json', posts)
    # epsg_json = json.loads(post_list.replace("\'", '"'))

    # with open('new_file.yml', 'w') as f:
    #     yaml.dump(epsg_json, f, indent=0)

    with open('/home/rutujakadam/Downloads/hr_faq_data1.json') as js:
        data = json.load(js)
    
    with open('new_file.yml', 'w') as yml:
        yaml.dump(data, yml, allow_unicode=True)
    return HttpResponse("doneeeeeeeeeeee")
