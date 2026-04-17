from django.views import View
from django.shortcuts import render, redirect

class BlogDetailsView(View):
    def get(self, request):

        context = {
           'TitleSearch' : True
        }

        return render(request, 'blog/blog-details.html', context)