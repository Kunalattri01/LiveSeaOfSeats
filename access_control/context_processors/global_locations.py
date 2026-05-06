from venues.models import City
from django.db.models import F

def global_cities(request):
    return {
        'all_cities': City.objects.filter(is_active = True).values('id', 'name').order_by('name')
    }

def global_countries(request):

    countries = (
        City.objects.filter(is_active=True).exclude(country_code__isnull=True).exclude(country_code='').values('country_name','country_code').distinct().order_by('country_name')
    )

    return {
        'all_countries': countries
    }