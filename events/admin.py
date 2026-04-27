from django.contrib import admin
from .models import Event, EventSpeaker, EventFAQ, EventSponsor, EventMedia, TicketMode, Category, EventTag, Language, ShowTime

# Register your models here.
admin.site.register(Event)
admin.site.register(EventSpeaker)
admin.site.register(EventFAQ)
admin.site.register(EventSponsor)
admin.site.register(EventMedia)
admin.site.register(TicketMode)
admin.site.register(Category)
admin.site.register(EventTag)
admin.site.register(Language)
admin.site.register(ShowTime)