from django.views import View
from django.shortcuts import render, redirect

class MovieTicketPlanView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'website/movies/movie-ticket-plan.html', context)