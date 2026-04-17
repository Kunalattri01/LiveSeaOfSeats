from django.db import models

class TicketType(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    # event = models.ForeignKey(Event, on_delete=models.CASCADE, db_column='EVENT_ID', related_name='event_tickets')
    show = models.ForeignKey('booking.ShowTime', on_delete=models.CASCADE, db_column='SHOWTIME_ID', related_name='event_tickets')
    name = models.CharField(max_length=100, db_column='NAME')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='PRICE')
    sold = models.IntegerField(default=0, db_column='SOLD')
    # remaining = models.IntegerField(default=0, db_column='REMAINING')
    locked = models.IntegerField(default=0, db_column='LOCKED')
    color = models.CharField(max_length=20, blank=True, db_column='COLOR')
    quantity = models.IntegerField(db_column='QUANTITY')
    description = models.TextField(db_column='DESCRIPTION')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT' )

    # def __str__(self):
    #     return f"{self.name} - {self.event.title}"

    class Meta:
        db_table = 'TICKET_TYPE_MT'