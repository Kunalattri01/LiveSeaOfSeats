from django.db import models
from django.db.models import Q
from .mdl_city import *

class Venue(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    external_id = models.CharField(max_length=100, null=True, blank=True, db_column='EXTERNAL_ID', db_index=True)
    source = models.CharField(max_length=50, null=True, blank=True, db_column='SOURCE', db_index=True)
    name = models.CharField(max_length=255, db_column='NAME', db_index=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, db_column='CITY_ID')
    address = models.TextField(db_column='ADDRESS', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column='LATITUDE')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_column='LONGITUDE')
    capacity = models.IntegerField(null=True, blank=True, db_column='CAPACITY')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        db_table = 'VENUE_MT'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'city'],
                name='unique_venue_per_city'
            ),
            models.UniqueConstraint(
                fields=['external_id', 'source'],
                condition=Q(external_id__isnull=False, source__isnull=False),
                name='unique_external_source'
            )
        ]
        indexes = [
            models.Index(fields=['external_id', 'source']),
            models.Index(fields=['name', 'city']),
        ]