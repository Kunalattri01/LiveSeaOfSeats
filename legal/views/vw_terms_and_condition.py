from django.views import View
from django.shortcuts import render, redirect

class TermsView(View):
    def get(self, request):

        context = {
            'TitleSearch' : True,
            'ask_user_mail' : True,
        }
                
        return render(request, 'website/legal/terms.html', context)