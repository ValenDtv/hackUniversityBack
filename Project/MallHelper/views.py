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


	@csrf_exempt
def create_rec(request):
    request_data = json.loads(request.body)
    place = places.objects.filter(placeid=request_data['placeid'])
    new_rec = recomendations(message=request_data['message'], placeid=place[0])
    new_rec.save()
    if (len(request_data['attributes'])>0):
        for attribut in request_data['attributes']:
            atr = attributes.objects.filter(attributeid=attribut)
            new_ar = recomendationsattributes(recomendationid=new_rec, attributeid=atr[0])
            new_ar.save()
    response = {'success': True, 'recomendationid': new_rec.recomendationid}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def update_rec(request):
    request_data = json.loads(request.body)
    recommendation = recomendations.objects.get(recomendationid=request_data['recommendationid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        recommendation.__dict__[field] = value
        recommendation.save()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def delete_rec(request):
    request_data = json.loads(request.body)
    recommendation = recomendations.objects.get(recomendationid=request_data['recommendationid'])
    recommendation.delete()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def select_rec(request):
    request_data = json.loads(request.body)
    recommens = recomendations.objects.filter(placeid=request_data['placeid'])
    response = {'success': True, 'recommendations': []}
    for recommen in recommens:
        r = {'message': recommen.message, 'attributes': []}
        attrs = recomendationsattributes.objects.filter(recomendationid=recommen)
        for a in attrs:
            r['attributes'].append(a.attributeid.attributeid)
        response['recommendations'].append(r)
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def select_allAttrs(request):
    attrs = attributes.objects.all()
    response = {'success': True, 'attributes': []}
    for attr in attrs:
        a = {}
        a['attributeid'] = attr.attributeid
        a['type'] = attr.type
        a['value'] = attr.value
        response['attributes'].append(a)
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)
	

	@csrf_exempt
def addRecommendationAttribute(request):
    request_data = json.loads(request.body)
    recomendation = recomendations.objects.get(recomendationid=request_data['recomendationid'])
    attribute = attributes.objects.get(attributeid=request_data['attributeid'])
    new_rec_attr = recomendationsattributes(recomendationid=recomendation, attributeid=attribute)
    new_rec_attr.save()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)


@csrf_exempt
def deleteRecommendationAttribute(request):
    request_data = json.loads(request.body)
    recomendation = recomendations.objects.get(recomendationid=request_data['recomendationid'])
    attribute = attributes.objects.get(attributeid=request_data['attributeid'])
    rec_attr = recomendationsattributes.objects.get(recomendationid=recomendation, attributeid=attribute)
    rec_attr.delete()
    response = {'success': True}
    response = json.dumps(response)
    return HttpResponse(response)