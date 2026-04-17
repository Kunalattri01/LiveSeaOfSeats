from django.db import models
from booking.models import Booking

class Payment(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='BOOKING_ID')
    payment_method = models.CharField(max_length=50, db_column='PAYMENT_METHOD')
    transaction_id = models.CharField(max_length=255, unique=True, db_column='TRANSACTION_ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_column='AMOUNT')
    status = models.CharField(max_length=50, db_column='STATUS')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')

    def __str__(self):
        return f"{self.transaction_id}"

    class Meta:
        db_table = 'PAYMENT_MT'