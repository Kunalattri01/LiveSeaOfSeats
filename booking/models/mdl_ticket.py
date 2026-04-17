from django.db import models
from .mdl_booking import Booking
from venues.models import Seat

class Ticket(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='BOOKING_ID')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, db_column='SEAT_ID')
    ticket_code = models.CharField(max_length=50, unique=True, db_column='TICKET_CODE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return self.ticket_code

    class Meta:
        db_table = 'TICKET_MT'