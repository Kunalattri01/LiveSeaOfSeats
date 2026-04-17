from django.db import models
from users.models import User
from .mdl_show_time import ShowTime

class Booking(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_ID')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, db_column='EVENT_ID')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, db_column='SHOWTIME_ID')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='TOTAL_AMOUNT')
    payment_id = models.CharField(max_length=100, null=True, blank=True, db_column='PAYMENT_ID')
    order_id = models.CharField(max_length=100, null=True, blank=True, db_column='ORDER_ID')
    qr_code = models.ImageField(upload_to="tickets/", null=True, blank=True, db_column='QR_CODE')
    qr_token = models.CharField(max_length=64, unique=True, null=True, blank=True, db_column='QR_TOKEN')
    is_used = models.BooleanField(default=False, db_column='IS_USED')
    status = models.CharField(max_length=20,
        choices=[
            ('LOCKED', 'Locked'),
            ('CONFIRMED', 'Confirmed'),
            ('FAILED', 'Failed'),
            ('EXPIRED', 'Expired')
        ],
        default='LOCKED', db_column='STATUS'
    )
    booking_time = models.DateTimeField(auto_now_add=True, db_column='BOOKING_TIME')

    def __str__(self):
        return f"Booking {self.id} - {self.user}"

    class Meta:
        db_table = 'BOOKING_MT'