from django.shortcuts import render
from .models import users
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