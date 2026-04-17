from django.views import View
from django.shortcuts import render, redirect

class ContactView(View):
    def get(self, request):

        context = {
            'TitleSearch': True
        }
        
        return render(request, 'contact/contact.html', context)