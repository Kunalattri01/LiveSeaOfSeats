from django.urls import path
from .views import *

urlpatterns = [
    path("suggestions/", SearchSuggestionView.as_view(), name="SearchSuggestionPage"),
]