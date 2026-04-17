from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieGridView.as_view(), name='MovieGridPage'),
    path('movie_details/', MovieDetailsView.as_view(), name='MovieDetailsPage'),
    path('movie_ticket_plan/', MovieTicketPlanView.as_view(), name='MovieTicketPlanPage'),
    path('movie_seat_plan/', MovieSeatPlanView.as_view(), name='MovieSeatPlanPage'),
    path('movie_checkout/', MovieCheckoutView.as_view(), name='MovieCheckoutPage'),
    path('beverages/', PopcornView.as_view(), name='PopcornPage'),
]