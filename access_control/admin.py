from django.contrib import admin
from .models import Menubar, PermissionList, Role, RolePermission, UserRole


# Register your models here.
admin.site.register(Menubar)
admin.site.register(PermissionList)
admin.site.register(Role)
admin.site.register(RolePermission)
admin.site.register(UserRole)