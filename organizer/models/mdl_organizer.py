from django.db import models 

class Organizer(models.Model):

    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='NAME')
    email = models.EmailField(db_column='EMAIL')
    phone = models.CharField(max_length=20, db_column='PHONE')
    website = models.URLField(blank=True, db_column='WEBSITE')
    instagram = models.URLField(blank=True, db_column='INSTAGRAM')
    facebook = models.URLField(blank=True, db_column='FACEBOOK')
    twitter = models.URLField(blank=True, db_column='TWITTER')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ORGANIZER_MT"