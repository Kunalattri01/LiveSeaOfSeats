from django.views import View
from django.shortcuts import render, redirect

class MovieDetailsView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True
        }

        return render(request, 'website/movies/movie-details.html', context)