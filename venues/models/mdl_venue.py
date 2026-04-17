from django.db import models
from .mdl_city import *

class Venue(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=255, db_column='NAME')
    city = models.ForeignKey(City, on_delete=models.CASCADE, db_column='CITY_ID')
    address = models.TextField(db_column='ADDRESS')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column='LATITUDE')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column='LONGITUDE')
    capacity = models.IntegerField(null=True, blank=True, db_column='CAPACITY')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'VENUE_MT'