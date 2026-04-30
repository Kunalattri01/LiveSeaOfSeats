from venues.models import City

def global_cities(request):
    return {
        'all_cities': City.objects.filter(is_active = True).values('id', 'name').order_by('name')
    }

def global_countries(request):
    return {
        'all_countries': City.objects.filter(is_active = True).values('country').order_by('country').distinct()
    }