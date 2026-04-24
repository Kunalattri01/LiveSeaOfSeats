from django.db import models

class Categories(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='NAME')
    slug = models.SlugField(unique=True, db_column='SLUG')
    tm_id = models.CharField(max_length=100, db_column='TM_ID', null=True, blank=True, help_text="Ticketmaster Segment/Genre ID")
    tm_param = models.CharField(max_length=50, db_column='TM_PARAM', default='segmentId', help_text="e.g., segmentId or genreId")
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'CATEGORIES'