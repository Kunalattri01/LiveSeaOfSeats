from django.db import models

class Category(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='NAME')
    slug = models.SlugField(db_column='SLUG')
    external_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    source = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'EVENT_CATEGORY'