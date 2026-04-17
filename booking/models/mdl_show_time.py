from django.db import models
from venues.models import Hall

class ShowTime(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, db_column='EVENT_ID')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, db_column='HALL_ID')
    show_date = models.DateField(db_column='SHOW_DATE', null=True, blank=True) 
    start_time = models.TimeField(db_column='START_TIME', null=True, blank=True)
    end_time = models.TimeField(db_column='END_TIME', null=True, blank=True)
    layout_image = models.ImageField(upload_to="venue_layouts/", blank=True, null=True, db_column='LAYOUT_IMAGE')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    # def __str__(self):
    #     return f"{self.event.title} - {self.start_time}"

    class Meta:
        db_table = 'SHOWTIME_MT'