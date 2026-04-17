from django.http import Http404
from django.http import JsonResponse

def permission_required(permission):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if permission not in request.base_rights:
                raise Http404()

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def api_permission_required(permission):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if permission not in request.base_rights:
                return JsonResponse(
                    {"error": "Permission denied"},
                    status=403
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator