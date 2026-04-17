from django.db import models
from .mdl_hall import *

class Seat(models.Model):
        
    id = models.AutoField(db_column='ID', primary_key=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, db_column='HALL_ID')
    row = models.CharField(max_length=5, db_column='ROW')
    number = models.IntegerField(db_column='NUMBER')
    seat_type = models.CharField(max_length=20, db_column='SEAT_TYPE')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"{self.row}{self.number}"
    
    class Meta:
        db_table = 'SEAT_MT'