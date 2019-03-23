from django.shortcuts import render
from .models import users
from .models import maps
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def register(request):
    request_data = json.loads(request.body)
    new_user = users(name=request_data['name'], password=request_data['password'], email=request_data['email'])
    new_user.save()
    response = {'success': True, 'userid': new_user.userid}
    response = json.dumps(response)
    return HttpResponse(response)
	

@csrf_exempt
def authorization(request):
    request_data = json.loads(request.body)
    #authResponse = authOutput()
    response = {'success': False, 'userid': 0}
    user = [u for u in users.objects.filter(email=request_data['email'], password=request_data['password'])]
    if (len(user)>0):
        response["success"] = True
        response["userid"] = user[0].userid
    #user = [u for u in users.objects.raw("Select * from users")]
    response = json.dumps(response)
    return HttpResponse(response)
	

@csrf_exempt
def create_map(request):
    request_data = json.loads(request.body)
    user = users.objects.get(userid=request_data['userid'])
    new_map = maps(name=request_data['name'], map=request_data['map'], level=request_data['level'],userid=user)
    new_map.save()
    response = {'success': True, 'mapid': new_map.mapid}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def update_map(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        map.__dict__[field] = value
        map.save()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)