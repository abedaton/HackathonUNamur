import BackEnd.server as backend
from django.contrib.auth.models import User

class SettingsBackend:
    def authenticate(self, request, **credentials):
        server = backend.Server
        server.handleEachUser()


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
