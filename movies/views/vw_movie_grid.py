from django.views import View
from django.shortcuts import render, redirect

class MovieGridView(View):
    def get(self, request):
        return render(request, 'movies/movie-grid.html')