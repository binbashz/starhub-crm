from django.urls import path
from .views import ProfileUpdateView

from . import views

app_name = 'userprofile'

urlpatterns = [
    path('myaccount/', views.myaccount, name='myaccount'),
    path('sign-up/', views.signup, name='signup'),
    path('log-in/', views.login, name='login'),
    path('myaccount/', views.ProfileUpdateView.as_view(), name='myaccount'),
      
]