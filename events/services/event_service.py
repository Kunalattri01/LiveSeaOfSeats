from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Min, F
from django.utils import timezone
from events.models import *
from booking.models import *

# -------------------------- [ vw_events ] --------------------------
def get_events_queryset(city):  # returns all the active events

    events = (
        Event.objects
        .filter(is_active=True, venue__city__name__iexact = city)
        .select_related('venue')
        .prefetch_related(
            Prefetch(
                'event_media',
                queryset=EventMedia.objects.filter(
                    media_type='thumbnail',
                    is_active=True
                ),
                to_attr='template_media'
            )
        )
        .order_by("start_date", "id")
    )
    return events



def get_events(event_type = None, city = None):

    events = get_events_queryset(city)

    if event_type == "upcoming":

        now = timezone.now()

        events = events.filter(
            status='PUBLISHED',
            release_date__lte=now,
            booking_start__gte=now,
            end_date__gte=now
        )

    return events


def get_filter_language(): # language filters
    return Language.objects.filter(is_active = True).order_by('seq_no')


def get_filter_categories(): # Categories filters
    return Categories.objects.filter(is_active = True)


def get_filter_eventtags(): # EventTag filters
    return EventTag.objects.filter(is_active = True)





# -------------------------- [ vw_event_details & vw_event_ticket ] ---------------------------

def get_event_details(event_id): # data related to selected event

    event = get_object_or_404(
        Event.objects
        .select_related('venue', 'category')
        .prefetch_related(

            # all images
            'event_media',

            # banner image
            Prefetch(
                'event_media',
                queryset=EventMedia.objects.filter(media_type='banner', is_active=True),
                to_attr='banner_media'
            ),

            # gallery images
            Prefetch(
                'event_media',
                queryset=EventMedia.objects.filter(media_type='gallery', is_active=True),
                to_attr='gallery_media'
            ),

            # thumbnail
            Prefetch(
                'event_media',
                queryset=EventMedia.objects.filter(media_type='thumbnail', is_active=True),
                to_attr='thumbnail_media'
            ),
        ),
        id=event_id
    )

    return event






# -------------------------- [ vw_event_details & vw_event_ticket ] ---------------------------

def get_event_layout(event_id): # event layout
    return ShowTime.objects.filter(event = event_id, is_active = True).values('layout_image').first()



def get_selected_faqs(event_id): # FAQs in a selected event
    return EventFAQ.objects.select_related('event').filter(event = event_id, is_active=True).order_by('seq_no')



def get_sponsors(event_id): # Sponsors details in a selected event
    return Sponsor.objects.select_related('event').filter(event = event_id, is_active = True)






# -------------------------- [ vw_event_details & vw_event_speaker ] ---------------------------

def get_speaker_details(event_id): # details of the speakers in an event
    return Speaker.objects.select_related('event').filter(event=event_id, is_active = True)


def selected_speaker_details(speaker_id):
    return Speaker.objects.filter(id = speaker_id).first()






# ---------------------- [ vw_event_ticket ] ----------------------

def get_ticket_category(show_id):
    return TicketType.objects.filter(is_active = True, show = show_id).select_related('show')





# ---------------------- [ vw_ticket_options & vw_event_checkout ] ----------------------

def get_ticket_rcv_mode(show_id): # Get Ticket Receving Mode ( M-Ticket, Email, Box-Office etc. )
    return ShowTime.objects.select_related('event', 'hall').filter(id = show_id, is_active = True).values(
        Ticket_Mode_Name = F('event__ticket_modes__name'), Ticket_Mode_Code = F('event__ticket_modes__code'), 
        Ticket_Mode_Description = F('event__ticket_modes__description'))



def get_event_ticket_summary(temp_booking_id): # Get Ticket Summary ( Total Ticket Booked, ShowTiming, Tickets Count etc. )
    result =  TempBookingItem.objects.select_related('temp_booking').filter(temp_booking__id = temp_booking_id).values(
            EventTitle = F('temp_booking__event__title'), Eventlanguage = F('temp_booking__event__languages__name'), 
            EventVenue = F('temp_booking__event__venue__name'), PurchasingQuantity = F('quantity'), EachTicketPrice = F('ticket_type__price'),
            EventDate =  F('ticket_type__show__show_date'), EventTime = F('ticket_type__show__start_time'),
            TicketCat = F('ticket_type__name')
        )

    for item in result:
        item['TotalTicketPrice'] = item['EachTicketPrice'] * item['PurchasingQuantity']

    return result






# --------------------- [ vw_event_timing ] -----------------------

def get_venues_list(event_id): # To get the Venues list of the selected event
    return (
        ShowTime.objects
        .select_related('hall__venue')
        .filter(event_id=event_id, is_active=True)
        .values(CityName = F('hall__venue__city__name'), VenueId = F('hall__venue__id'), VenueName = F('hall__venue__name'), StartTime = F('start_time'), EndTime = F('end_time'), ShowDate = F('show_date') ,VenueAddress = F('hall__venue__address'), ShowId = F('id'))  # include id
        .distinct()
    )



# --------------------- [ vw_payment_success ] ---------------------

def get_success_details(booking_id): # To show the details on Success and Page and Downloaded tickets

    return BookingItem.objects.select_related('booking').filter(booking__id = booking_id)