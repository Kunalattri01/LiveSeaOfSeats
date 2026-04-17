from django.db import models
from .mdl_event import Event

class EventMedia(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID', related_name='event_media')
    image = models.ImageField(upload_to="events/", db_column='IMAGE')

    media_type = models.CharField(
        max_length=20, db_column='MEDIA_TYPE',
        choices=[
            ('banner','Banner'),
            ('gallery','Gallery'),
            ('thumbnail','Thumbnail')
        ]
    )
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.event.title
    
    class Meta: 
        db_table = 'EVENT_MEDIA'