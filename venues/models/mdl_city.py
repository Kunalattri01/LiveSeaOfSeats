from django.db import models

class City(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='NAME')
    state = models.CharField(max_length=100, blank=True, db_column='STATE')
    country = models.CharField(max_length=100, db_column='COUNTRY')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'CITY_MT'