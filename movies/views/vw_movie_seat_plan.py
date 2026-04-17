from django.views import View
from django.shortcuts import render, redirect

class MovieSeatPlanView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'movies/movie-seat-plan.html', context)