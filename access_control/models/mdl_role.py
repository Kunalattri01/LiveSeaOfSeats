from django.db import models

class Role(models.Model):

    id = models.AutoField(primary_key=True, db_column="ID")
    role_code = models.CharField(max_length=50, unique=True, db_column="ROLE_CODE")
    role_name = models.CharField(max_length=100, db_column="ROLE_NAME")
    is_active = models.BooleanField(default=True, db_column="IS_ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CREATED_AT")

    def __str__(self):
        return self.role_name
    
    class Meta:
        db_table = "Role_MT"