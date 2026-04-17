from django.db import models
from users.models import User
from .mdl_show_time import ShowTime


class TempBooking(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='USER_ID')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, db_column='EVENT_ID')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, db_column='SHOWTIME_ID', null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    expires_at = models.DateTimeField(db_column='EXPIRES_AT')
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('EXPIRED', 'Expired'),
            ('CONSUMED', 'Used')
        ],
        default='ACTIVE'
    )
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')

    class Meta:
        db_table = 'TEMP_BOOKING'