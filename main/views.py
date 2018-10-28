from django.shortcuts import render
from django.template import RequestContext
from django.conf import settings
from .forms import LoginForm

# Create your views here.

from django.http import HttpResponse

def home(request):
    form = LoginForm(request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        print(form.cleaned_data['mail'])
    return render(request, "index.html", locals())

def map(request, postalCode):
    return render(request, "map.html")

def farmer_page(request):
    name = "Les produits de Sophie"
    return render(request, "farmer_page.html", {"FARMER_NAME":name})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
    pass
