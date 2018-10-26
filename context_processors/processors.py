from django.conf import settings

def appname(request):
    return {'APPNAME': settings.NAME}