from django.db import models

class Language(models.Model):
    
    id = models.AutoField(db_column='ID', primary_key=True)
    seq_no = models.IntegerField(db_column='SEQ_NO')
    name = models.CharField(max_length=50, db_column='NAME')
    tm_locale = models.CharField(max_length=10, db_column='TM_LOCALE', null=True, blank=True, help_text="e.g., 'en' or 'en-us'")
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'LANGUAGE'