from django.db import models
from users.models import User
from events.models import Event


class Review(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,db_column='USER_ID')
    event = models.ForeignKey(Event,on_delete=models.CASCADE,db_column='EVENT_ID')
    rating = models.IntegerField(db_column='RATING')
    comment = models.TextField(db_column='COMMENT')
    created_at = models.DateTimeField(auto_now_add=True,db_column='CREATED_AT')

    def __str__(self):
        return f"{self.user} - {self.event}"

    class Meta:
        db_table = 'REVIEW_MT'