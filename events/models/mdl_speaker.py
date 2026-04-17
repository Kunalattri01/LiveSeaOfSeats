from django.db import models
from .mdl_event import Event

class Speaker(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    seq_no = models.IntegerField(db_column='SEQ_NO')
    name = models.CharField(max_length=255, db_column='NAME')
    bio = models.TextField(blank=True, db_column='BIO')
    image = models.ImageField(upload_to="speakers/", db_column='IMAGE')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID')
    role = models.CharField(max_length=20,
        choices=[
            ("ARTIST", "Artist"),
            ("SPEAKER", "Speaker")
        ], db_column="ROLE"
    )
    performance_time = models.TimeField(null=True, blank=True, db_column="PERFORMANCE_TIME")
    website = models.URLField(blank=True, db_column='WEBSITE')
    instagram = models.URLField(blank=True, db_column='INSTAGRAM')
    facebook = models.URLField(blank=True, db_column='FACEBOOK')
    twitter = models.URLField(blank=True, db_column='TWITTER')
    description = models.TextField(db_column='DESCRIPTION')
    email = models.EmailField(db_column='EMAIL', null=True, blank=True)
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'SPEAKER_MT'