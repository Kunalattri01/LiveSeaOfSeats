from django.db import models
from .mdl_menubar import *

class PermissionList(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    menu_code = models.ForeignKey(Menubar, on_delete=models.CASCADE, to_field='menu_code', db_column='MENU_CODE', blank=True, null=True)
    perm_code = models.CharField(max_length=45, db_column='PERM_CODE', unique=True)
    perm_type = models.CharField(max_length=150, choices=[
        ('BASE', 'BASE'),
        ('SPECIAL', 'SPECIAL')
    ], db_column='PERM_TYPE')
    perm_name = models.CharField(max_length=55, db_column='PERM_NAME')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"{self.perm_name}"

    class Meta: 
        db_table = 'PermissionList_MT'