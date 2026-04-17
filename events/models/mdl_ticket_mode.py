from django.db import models

class TicketMode(models.Model):

    id = models.AutoField(primary_key=True, db_column='ID')
    code = models.CharField(max_length=20, unique=True, db_column='CODE')  # qr, email, boxoffice
    name = models.CharField(max_length=100, db_column='NAME')
    icon = models.CharField(max_length=50, blank=True, db_column='ICON')  # fa-qrcode
    description = models.TextField(blank=True, db_column='DESCRIPTION')

    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TICKET_MODE_MT'