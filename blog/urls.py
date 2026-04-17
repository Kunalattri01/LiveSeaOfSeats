from django.urls import path
from .views import *

urlpatterns = [
    path('', BlogView.as_view(), name='BlogPage'),
    path('blog_details/', BlogDetailsView.as_view(), name='BlogDetailsPage'),
]