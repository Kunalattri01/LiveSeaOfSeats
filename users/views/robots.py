from django.http import HttpResponse

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow: /",
        content_type="text/plain"
    )