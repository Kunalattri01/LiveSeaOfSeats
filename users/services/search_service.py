from django.db.models import Q
from events.models import *

def global_search(queryset, query):

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

        if not queryset:
            print('hhhhhh')
            queryset = {
                'events': []
            }
    print('queryset : ', queryset)
    return queryset