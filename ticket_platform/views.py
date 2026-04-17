from django.shortcuts import render

def custom_404(request, exception):
    return render(request, "404.html", {
        "HeaderSection": True,
        "TitleSearch": True
    }, status=404)