from django.db import models
from .mdl_event import Event

class EventFAQ(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    seq_no = models.IntegerField(db_column='SEQ_NO')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID')
    question = models.CharField(max_length=255, db_column='QUESTION')
    answer = models.TextField(db_column='ANSWER')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'EVENT_FAQ_MT'