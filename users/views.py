from django.contrib.auth.backends import BaseBackend
from Registration.models import Registation # Replace with your actual user model
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
USER = get_user_model()

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

USER = get_user_model()

class AuthenticationBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(USER.USERNAME_FIELD)
        
        if username is None or password is None:
            return None  # Both username and password are required for authentication.
        #print(username,password)
        try:
            username = username.strip()
            user = USER._default_manager.get(Q(username__iexact=username) | Q(email__iexact=username))
            #print(user, 'here is the user')
        except USER.DoesNotExist:
            return None  # User does not exist.
        #print(user, 'hello to may world')
        if user.check_password(password) :
            return user

    def get_user(self, user_id):
        try:
            return USER._default_manager.get(pk=user_id)
        except USER.DoesNotExist:
            return None
        
    

"""class AuthentificationBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        if username is None:
            username = kwargs.get(USER.USERNAME_FIELD)

        
        print(username,password)
        users = USER._default_manager.filter(
            Q(username__iexact=username) | Q(email__iexact=username))
        print(users)
        for user in users:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        if not users:
           
            USER().set_password(password)
    class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Registation.objects.get(username=username)
            if user.check_password(password):
                return user
        except Registation.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Registation.objects.get(pk=user_id)
        except Registation.DoesNotExist:
            return None
"""