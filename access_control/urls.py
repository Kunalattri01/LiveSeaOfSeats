from django.urls import path
from .views import *

urlpatterns = [
    path('menubar_entry/', MenubarEntryView.as_view(), name='MenubarEntryPage'),
    path("permissionlist/", PermissionEntryView.as_view(), name="PermissionEntryPage"),
]