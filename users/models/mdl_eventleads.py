from django.db import models
from events.models import Event

class EventLead(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, db_column='EVENT_ID')
    name = models.CharField(max_length=150, db_column='NAME')
    email = models.EmailField(db_column='EMAIL')
    phone = models.CharField(max_length=20, db_column='PHONE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'EVENT_LEAD'