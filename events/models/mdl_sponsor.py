from django.db import models
from .mdl_event import Event


class Sponsor(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID')
    name = models.CharField(max_length=255, db_column='NAME')
    logo = models.ImageField(upload_to="sponsors/", db_column='LOGO')
    website = models.URLField(blank=True, db_column='WEBSITE')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'SPONSOR_MT'