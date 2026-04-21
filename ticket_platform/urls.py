"""ticket_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ticketmaster.urls')), # comment it in future (make change in header component)
    path('users/', include('users.urls')),  # make it '' in future 
    path('events/', include('events.urls')),
    path('sports/', include('sports.urls')),
    path('movies/', include('movies.urls')),
    path('contact/', include('contact.urls')),
    path('blog/', include('blog.urls')),
    path('access_control/', include('access_control.urls')),
    path("search/", include("search.urls")),
    # path('ticketmaster/', include('ticketmaster.urls')), # remove comment in future
]

handler404 = "ticket_platform.views.custom_404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)