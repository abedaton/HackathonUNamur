from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name="home"),
    path('map/<int:postalCode>', views.map, name="map"),
    path('farmer_page', views.farmer_page, name="farmer_page"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('login', views.login, name="login")
]
