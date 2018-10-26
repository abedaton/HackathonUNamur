from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings

# Create your views here.

from django.http import HttpResponse

def home(request):
    print(settings.NAME)
    return render(request, "index.html")
