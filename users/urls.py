from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='HomePage'),
    path('sign_up/', SignUpView.as_view(), name='SignUpPage'),
    path('sign_in/', SignInView.as_view(), name='SignInPage'),
    path('set-city/', SetCityView.as_view(), name='SetCity'),
    path("robots.txt", robots_txt),
]