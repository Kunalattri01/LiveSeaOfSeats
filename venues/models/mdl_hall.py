from django.db import models
from .mdl_venue import *

class Hall(models.Model):
        
    id = models.AutoField(db_column='ID', primary_key=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, db_column='VENUE_ID')
    name = models.CharField(max_length=100, db_column='NAME')
    total_seats = models.IntegerField(db_column='TOTAL_SEATS')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"{self.venue.name} - {self.name}"
    
    class Meta:
        db_table = 'HALL_MT'