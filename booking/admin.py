from django.contrib import admin
from .models import ShowTime, Booking, Ticket, BookingItem, TicketType

# Register your models here.
admin.site.register(ShowTime)
admin.site.register(Booking)
admin.site.register(Ticket)
admin.site.register(BookingItem)
admin.site.register(TicketType)
