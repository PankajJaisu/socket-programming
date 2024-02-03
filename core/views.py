from django.shortcuts import render
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def get_last_session_data(request):
    session = Session.objects.filter().last()
   
    session_key = session.session_key
    session_data = session.session_data
    result = SessionStore(session_key).decode(session_data)
    return JsonResponse({"session_data":result})