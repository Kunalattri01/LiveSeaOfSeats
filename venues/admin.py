from django.contrib import admin
from .models import City, Venue, Hall, Seat

# Register your models here.
admin.site.register(City)
admin.site.register(Venue)
admin.site.register(Hall)
admin.site.register(Seat)