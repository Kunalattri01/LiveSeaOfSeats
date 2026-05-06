from django.db import models
from django.db.models import Q

from venues.models import Hall, Venue
from .mdl_event import Event

class ShowTime(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID')
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, blank=True, db_column='HALL_ID')
    match_title = models.CharField(max_length=255, null=True, blank=True)
    show_date = models.DateField(db_column='SHOW_DATE', null=True, blank=True)
    start_time = models.TimeField(db_column='START_TIME', null=True, blank=True)
    end_time = models.TimeField(db_column='END_TIME', null=True, blank=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, db_column='VENUE_ID')
    layout_image = models.ImageField(upload_to="venue_layouts/", blank=True, null=True, db_column='LAYOUT_IMAGE')
    layout_image_url = models.URLField(null=True, blank=True, db_column='LAYOUT_IMAGE_URL')
    external_id = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    booking_url = models.URLField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('SCHEDULED', 'SCHEDULED'),
            ('CANCELLED', 'CANCELLED'),
            ('RESCHEDULED', 'RESCHEDULED'),
            ('SOLD_OUT', 'SOLD_OUT'),
            ('COMPLETED', 'COMPLETED'),
        ],
        default='SCHEDULED'
    )
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    class Meta:
        db_table = 'SHOWTIME_MT'
        constraints = [
            models.UniqueConstraint(
                fields=['external_id', 'source'],
                condition=Q(external_id__isnull=False, source__isnull=False),
                name='unique_showtime_external_source'
            )
        ]
        indexes = [
            models.Index(fields=['event', 'show_date']),
            models.Index(fields=['external_id', 'source']),
        ]