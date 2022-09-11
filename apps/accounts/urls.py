# imports
from django.urls import include, path

from . import views

app_name = 'Auth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login' ),
    path('register/', views.RegisterUser.as_view(), name='register' ),
    path('verify/', views.VerifyUser.as_view(), name='verify' ),
]
