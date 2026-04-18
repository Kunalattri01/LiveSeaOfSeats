from django.http import HttpResponse
import base64
import os

class BasicAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION')

        USERNAME = os.environ.get("SITE_USER", "admin")
        PASSWORD = os.environ.get("SITE_PASS", "5555")

        if auth:
            try:
                method, encoded = auth.split(' ', 1)
                if method.lower() == 'basic':
                    decoded = base64.b64decode(encoded).decode('utf-8')
                    username, password = decoded.split(':', 1)

                    if username == USERNAME and password == PASSWORD:
                        return self.get_response(request)
            except:
                pass

        response = HttpResponse('Unauthorized', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Restricted"'
        return response