from django.db import models

class City(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=100, db_column='NAME', db_index=True)
    state_name = models.CharField(max_length=100, null=True, blank=True, db_column='STATE_NAME')
    state_code = models.CharField(max_length=20, null=True, blank=True, db_column='STATE_CODE')
    country_name = models.CharField(max_length=100, db_column='COUNTRY_NAME')
    country_code = models.CharField(max_length=20, null=True, blank=True, db_column='COUNTRY_CODE')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):

        state = (
            f"{self.state_name} ({self.state_code})"
            if self.state_name or self.state_code
            else ""
        )

        country = (
            f"{self.country_name} ({self.country_code})"
            if self.country_name or self.country_code
            else ""
        )

        return f"{self.name}, {state}, {country}"
    
    class Meta:
        db_table = 'CITY_MT'
        unique_together = ('name', 'state_code', 'country_code')