from django.db import models

class Menubar(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    position = models.IntegerField(db_column='POSITION', null=True, blank=True)
    menu_code = models.CharField(max_length=100, db_column = 'MENU_CODE', unique=True)
    menu_name = models.CharField(max_length=100, db_column = 'MENU_NAME')
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null=True, blank=True, db_column="PARENT", related_name='children')
    # has_parent = models.BooleanField(default=False, db_column='HAS_PARENT')
    # has_child = models.BooleanField(default=False, db_column = 'HAS_CHILD')
    url = models.CharField(max_length = 150, db_column="URL", blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, db_column="ICON")
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.menu_name
    
    class Meta:
        db_table = 'MENUBAR_MT'