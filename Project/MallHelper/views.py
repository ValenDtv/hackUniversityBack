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
    response = json.dumps(response, ensure_ascii=False)
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
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def update_rec(request):
    request_data = json.loads(request.body)
    recomendation = recomendations.objects.get(recomendationid=request_data['recomendationid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        recomendation.__dict__[field] = value
        recomendation.save()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def delete_rec(request):
    request_data = json.loads(request.body)
    recomendation = recomendations.objects.get(recomendationid=request_data['recomendationid'])
    recomendation.delete()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def select_rec(request):
    request_data = json.loads(request.body)
    recomens = recomendations.objects.filter(placeid=request_data['placeid'])
    response = {'success': True, 'recomendations': []}
    for recomen in recomens:
        r = {'recomendationid': recomen.recomendationid,'message': recomen.message, 'attributes': []}
        attrs = recomendationsattributes.objects.filter(recomendationid=recomen)
        for a in attrs:
            r['attributes'].append(a.attributeid.attributeid)
        response['recomendations'].append(r)
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
        a['in_client'] = attr.in_client
        response['attributes'].append(a)
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def create_place(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    new_place = places(x=request_data['x'], y=request_data['y'], name=request_data['name'], mapid=map)
    new_place.save()
    response = {'success': True, 'place':new_place.placeid}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def update_place(request):
    request_data = json.loads(request.body)
    place = places.objects.get(placeid=request_data['placeid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        place.__dict__[field] = value
        place.save()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def delete_place(request):
    request_data = json.loads(request.body)
    place = places.objects.get(placeid=request_data['placeid'])
    place.delete()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
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
def create_map(request):
    request_data = json.loads(request.body)
    user = users.objects.get(userid=request_data['userid'])
    new_map = maps(name=request_data['name'], map=request_data['map'], level=request_data['level'],userid=user)
    new_map.save()
    response = {'success': True, 'mapid': new_map.mapid}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def update_map(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    for field, value in zip(request_data['fields'], request_data['values']):
        map.__dict__[field] = value
        map.save()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)


@csrf_exempt
def delete_map(request):
    request_data = json.loads(request.body)
    map = maps.objects.get(mapid=request_data['mapid'])
    map.delete()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
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
def addRecomendationAttribute(request):
    request_data = json.loads(request.body)
    recomendation = recomendations.objects.get(recomendationid=request_data['recomendationid'])
    attribute = attributes.objects.get(attributeid=request_data['attributeid'])
    new_rec_attr = recomendationsattributes(recomendationid=recomendation, attributeid=attribute)
    new_rec_attr.save()
    response = {'success': True}
    response = json.dumps(response, ensure_ascii=False)
    return HttpResponse(response)
	

def age_groups(human_age):
    age_attrs = attributes.objects.filter(type="age").exclude(value="any")
    age = {}
    for age_attr in age_attrs:
        gap = [int(a) for a in age_attr.value.split(',')]
        age[age_attr.value] = gap
    hits = []
    for key,a in age.items():
        if (a[0] < human_age < a[1]):
            hits.append(key)
    return hits


def age_analys(human_age, level):
    if (str(human_age) == 'any'):
        return recomendations.objects.filter(recomendationsattributes__attributeid__type="age",
                                             placeid__mapid__level=level)
    hits = age_groups(human_age)
    recomends1 = recomendations.objects.filter(recomendationid=0)
    for h in hits:
        r = recomendations.objects.filter(recomendationsattributes__attributeid__type="age",
                                          recomendationsattributes__attributeid__value=h, placeid__mapid__level=level)
        recomends1 = recomends1.union(r)
    recomends2 = recomendations.objects.filter(recomendationsattributes__attributeid__type="age",
                                          recomendationsattributes__attributeid__value="any",
                                               placeid__mapid__level=level)
    return recomends1.union(recomends2)


def gender_analys(human_gender, level):
    if (human_gender == 'any'):
        return recomendations.objects.filter(recomendationsattributes__attributeid__type="sex",
                                             placeid__mapid__level=level)
    recomends1 = recomendations.objects.filter(recomendationsattributes__attributeid__type="sex",
                                      recomendationsattributes__attributeid__value=human_gender,
                                               placeid__mapid__level=level)
    recomends2 = recomendations.objects.filter(recomendationsattributes__attributeid__type="sex",
                                          recomendationsattributes__attributeid__value="any",
                                               placeid__mapid__level=level)
    return recomends1.union(recomends2)


def race_analys(human_race, level):
    if (human_race == 'any'):
        return recomendations.objects.filter(recomendationsattributes__attributeid__type="race",
                                             placeid__mapid__level=level)
    recomends1 = recomendations.objects.filter(recomendationsattributes__attributeid__type="race",
                                      recomendationsattributes__attributeid__value=human_race,
                                               placeid__mapid__level=level)
    recomends2 = recomendations.objects.filter(recomendationsattributes__attributeid__type="race",
                                          recomendationsattributes__attributeid__value="any",
                                               placeid__mapid__level=level)
    return recomends1.union(recomends2)


def party_analys(humans_f, level):
    recomends_f = recomendations.objects.filter(recomendationid=0)
    recomends_f = recomendations.objects.filter(recomendationsattributes__attributeid__type="groups",
                                                recomendationsattributes__attributeid__value="party",
                                                placeid__mapid__level=level)
    return recomends_f


def lovers_analys(humans_f, level):
    recomends_f = recomendations.objects.filter(recomendationid=0)
    if (len(humans_f) != 2):
        return recomends_f
    human1_gender = humans_f[0]['data']['face']['gender_appearance']['concepts'][0]['name']
    human2_gender = humans_f[1]['data']['face']['gender_appearance']['concepts'][0]['name']
    if (human1_gender == human2_gender):
        return recomends_f
    human1_age = int(humans_f[0]['data']['face']['age_appearance']['concepts'][0]['name'])
    human2_age = int(humans_f[1]['data']['face']['age_appearance']['concepts'][0]['name'])
    if (abs(human1_age - human2_age)>10):
        return recomends_f
    recomends_f = recomendations.objects.filter(recomendationsattributes__attributeid__type="groups",
                                                recomendationsattributes__attributeid__value="lovers",
                                                placeid__mapid__level=level)
    return recomends_f


def family_analys(humans_f, level):
    recomends_f = recomendations.objects.filter(recomendationid=0)
    for human in humans_f:
        age = int(human['data']['face']['age_appearance']['concepts'][0]['name'])
        for another in humans_f:
            if (abs(age - int(another['data']['face']['age_appearance']['concepts'][0]['name']))>10):
                recomends_f = recomendations.objects.filter(recomendationsattributes__attributeid__type="groups",
                                                            recomendationsattributes__attributeid__value="family",
                                                            placeid__mapid__level=level)
    return recomends_f

	
def lovers_analys(humans_f, level):
    recomends_f = recomendations.objects.filter(recomendationid=0)
    if (len(humans_f) != 2):
        return recomends_f
    human1_gender = humans_f[0]['data']['face']['gender_appearance']['concepts'][0]['name']
    human2_gender = humans_f[1]['data']['face']['gender_appearance']['concepts'][0]['name']
    if (human1_gender == human2_gender):
        return recomends_f
    human1_age = int(humans_f[0]['data']['face']['age_appearance']['concepts'][0]['name'])
    human2_age = int(humans_f[1]['data']['face']['age_appearance']['concepts'][0]['name'])
    if (abs(human1_age - human2_age)>10):
        return recomends_f
    recomends_f = recomendations.objects.filter(recomendationsattributes__attributeid__type="groups",
                                                recomendationsattributes__attributeid__value="lovers",
                                                placeid__mapid__level=level)
    return recomends_f


def family_analys(humans_f, level):
    recomends_f = recomendations.objects.filter(recomendationid=0)
    for human in humans_f:
        age = int(human['data']['face']['age_appearance']['concepts'][0]['name'])
        for another in humans_f:
            if (abs(age - int(another['data']['face']['age_appearance']['concepts'][0]['name']))>10):
                recomends_f = recomendations.objects.filter(recomendationsattributes__attributeid__type="groups",
                                                            recomendationsattributes__attributeid__value="family",
                                                            placeid__mapid__level=level)
    return recomends_f


def dominate_age(humans):
    age_attrs = attributes.objects.filter(type="age").exclude(value="any")
    age_gaps = {}
    for age_attr in age_attrs:
        age_gaps[age_attr.value] = 0
    for human in humans:
        age = int(human['data']['face']['age_appearance']['concepts'][0]['name'])
        human_age_gaps = age_groups(age)
        for gap in human_age_gaps:
            age_gaps[gap] += 1
    result = [int(g) for g in max(age_gaps, key=lambda k: age_gaps[k]).split(',')]
    return sum(result)/len(result)
	
	
def dominate_gender(humans):
    genders = {'masculine': 0, 'feminine': 0}
    for human in humans:
        genders[human['data']['face']['gender_appearance']['concepts'][0]['name']] += 1
    return max(genders, key=lambda k: genders[k])

