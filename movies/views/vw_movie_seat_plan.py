from django.views import View
from django.shortcuts import render, redirect

class MovieSeatPlanView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'website/movies/movie-seat-plan.html', context)