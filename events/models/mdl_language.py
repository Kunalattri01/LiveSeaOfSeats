from django.db import models

class Language(models.Model):
    
    id = models.AutoField(db_column='ID', primary_key=True)
    seq_no = models.IntegerField(db_column='SEQ_NO')
    name = models.CharField(max_length=50, db_column='NAME')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'LANGUAGE'