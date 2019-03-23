from django.shortcuts import render
from .models import users
from .models import maps
from .models import places
from .models import recomendations
from .models import attributes
from .models import recomendationsattributes
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


@csrf_exempt
def delete_map(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    map.delete()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def select_maps(request):
    request_data = json.loads(request.body)
    user = users.objects.get(userid=request_data['userid'])
    user_maps = maps.objects.filter(userid=user)
    response = {'success': True, 'maps': []}
    for map in user_maps:
        m = {}
        m['mapid'] = map.mapid
        m['level'] = map.level
        m['map'] = map.map
        m['name'] = map.name
        m['userid'] = map.userid.userid
        response['maps'].append(m)
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)	

	
@csrf_exempt
def create_place(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    new_place = places(x=request_data['x'], y=request_data['y'], name=request_data['name'], mapid=map)
    new_place.save()
    response = {'success': True, 'place':new_place.placeid}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def update_place(request):
    request_data = json.loads(request.body)
    place = places.objects.get(placeid=request_data['placeid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        place.__dict__[field] = value
        place.save()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def delete_place(request):
    request_data = json.loads(request.body)
    place = places.objects.get(placeid=request_data['placeid'])
    place.delete()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def select_places(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    maps_places = places.objects.filter(mapid=map)
    response = {'success': True, 'places': []}
    for place in maps_places:
        p = {}
        p['placeid'] = place.placeid
        p['x'] = place.x
        p['y'] = place.y
        p['name'] = place.name
        p['mapid'] = place.mapid.mapid
        response['places'].append(p)
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)

