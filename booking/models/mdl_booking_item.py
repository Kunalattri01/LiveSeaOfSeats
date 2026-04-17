from django.db import models
from .mdl_booking import Booking
from .mdl_ticket_type import TicketType

class BookingItem(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='BOOKING_ID')
    category = models.ForeignKey(TicketType, on_delete=models.CASCADE, db_column='TICKET_TYPE_ID')
    quantity = models.IntegerField(db_column='QUANTITY')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='PRICE')
    ticket_id = models.CharField(max_length=100, unique=True, null=True, db_column='TICKET_ID')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    class Meta:
        db_table = 'BOOKING_ITEM'