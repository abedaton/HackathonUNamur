from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings

# Create your views here.

from django.http import HttpResponse

def home(request):
    return render(request, "index.html")

def map(request, postalCode):
    return render(request, "map.html")

def farmer_page(request):
    name = "Les produits de Sophie"
    return render(request, "farmer_page.html", {"FARMER_NAME":name})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")
