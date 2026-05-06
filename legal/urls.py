from django.urls import path
from .views import *

urlpatterns = [
    path('terms_conditions/', TermsView.as_view(), name='TermsPage'),
]