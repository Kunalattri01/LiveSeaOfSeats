from django.contrib import admin
from .models import Event, Speaker, EventFAQ, Sponsor, EventMedia, TicketMode

# Register your models here.
admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(EventFAQ)
admin.site.register(Sponsor)
admin.site.register(EventMedia)
admin.site.register(TicketMode)