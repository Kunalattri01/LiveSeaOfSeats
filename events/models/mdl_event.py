from django.db import models
from venues.models import Venue
from organizer.models import Organizer
from .mdl_event_category import Category
from .mdl_language import Language
from .mdl_event_tag import EventTag
from .mdl_ticket_mode import *
from django.db.models import Q

class Event(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    title = models.CharField(max_length=255, db_column='TITLE', db_index=True)
    slug = models.SlugField(db_column='SLUG', max_length=255, db_index=True)
    description = models.TextField(db_column='DESCRIPTION')

    age_limit = models.IntegerField(null=True, blank=True, db_column='AGE_LIMIT')
    release_date = models.DateTimeField(null=True, blank=True, db_column='RELEASE_DATE')
    booking_start = models.DateTimeField(null=True, blank=True, db_column='BOOKING_START')

    # start_date = models.DateTimeField(db_column='START_DATE', db_index=True)
    # end_date = models.DateTimeField(db_column='END_DATE')
    # venue = models.ForeignKey(Venue, on_delete=models.CASCADE, db_column='VENUE_ID') # just removed to show the multiple venue for a event (like year tour of a artist)

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, db_column="ORGANIZER_ID")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='CATEGORY_ID')

    languages = models.ManyToManyField(Language, blank=True)
    tags = models.ManyToManyField(EventTag, blank=True)

    youtube_url = models.URLField(blank=True, null=True, db_column='YOUTUBE_URL')
    terms_and_conditions = models.TextField(blank=True, db_column='TERMS')
    refund_policy = models.TextField(blank=True, db_column='REFUND_POLICY')
    
    status = models.CharField(
        max_length=20, db_column='STATUS',
        choices=[
            ('DRAFT','DRAFT'),
            ('PUBLISHED','PUBLISHED'),
            ('CANCELLED','CANCELLED'),
            ('ENDED','ENDED')
        ]
    )

    ticket_modes = models.ManyToManyField(TicketMode, blank=True)

    source_type = models.CharField(
        max_length=20,
        choices=[
            ("INTERNAL", "INTERNAL"),
            ("EXTERNAL", "EXTERNAL")
        ],
        default="INTERNAL"
    )

    external_id = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True, db_index=True)

    # delivery_mode = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ('qr', 'Mobile QR Ticket'),
    #         ('email', 'Email Ticket'),
    #         ('boxoffice', 'Box Office Pickup')
    #     ],
    #     default='qr',
    #     db_column='DELIVERY_MODE'
    # )

    # city = models.ForeignKey(City, on_delete=models.CASCADE, db_column='CITY_ID')
    # banner = models.ImageField(upload_to="events/", db_column='BANNER')
    is_active = models.BooleanField(default=True, db_column='IS_ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True, db_column='CREATED_AT')
    updated_at = models.DateTimeField(auto_now=True, db_column='UPDATED_AT')


    def __str__(self):
        return self.title
    
    class Meta: 
        db_table = 'EVENT_MT'
        constraints = [
            models.UniqueConstraint(
                fields=['external_id', 'source'],
                condition=Q(external_id__isnull=False, source__isnull=False),
                name='unique_event_external_source'
            )
        ]