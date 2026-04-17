from django.views import View
from django.shortcuts import render, redirect

class MovieDetailsView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'movies/movie-details.html', context)