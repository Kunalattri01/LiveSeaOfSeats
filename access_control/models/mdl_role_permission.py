from django.db import models
from .mdl_role import *
from .mdl_permission_list import *
from .mdl_menubar import *

class RolePermission(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    role_code = models.ForeignKey(Role, on_delete=models.CASCADE, to_field='role_code', db_column='ROLE_CODE')
    menu_code = models.ForeignKey(Menubar, on_delete=models.CASCADE, to_field='menu_code', db_column='MENU_CODE')
    perm_code = models.ForeignKey(PermissionList, on_delete=models.CASCADE, to_field='perm_code', db_column='PERM_CODE')
    is_allowed = models.BooleanField(default=True, db_column="IS_ALLOWED")

    class Meta:
        db_table = "RolePermission_MT"
