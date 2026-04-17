from django.urls import path
from .views import *

urlpatterns = [
    path('', SportsView.as_view(), name='SportsPage'),
]