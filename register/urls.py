from django.urls import path, include
from .views import *

urlpatterns = [
    path('', pageProfile, name='profile'), 
    path('settings/', pageSettings, name='settings'), 
    path('sign-up/', pageSignup, name='sign_up'), 
    path('sign-in/', pageSignin, name='sign_in'), 
    path('logout/', pageSignin, name='logout'), 
] 
