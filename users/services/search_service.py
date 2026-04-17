from django.db.models import Q
from events.models import *

def global_search(queryset, query):

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return queryset