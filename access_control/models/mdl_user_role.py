from django.db import *
from users.models import *
from .mdl_role import *

class UserRole(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="USER_ID")
    role_code = models.ForeignKey(Role, on_delete=models.CASCADE, to_field='role_code', db_column="ROLE_CODE")
    is_active = models.BooleanField(default=True, db_column="IS_ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CREATED_AT")

    class Meta:
        db_table = "UserRole_MT"