from django.db import models
from .mdl_temp_booking import TempBooking
from .mdl_ticket_type import TicketType

class TempBookingItem(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    temp_booking = models.ForeignKey(TempBooking, on_delete=models.CASCADE, db_column='TEMP_BOOKING_ID')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, db_column='TICKET_TYPE_ID')
    quantity = models.IntegerField(db_column='QUANTITY')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')

    class Meta:
        db_table = 'TEMP_BOOKING_ITEM'