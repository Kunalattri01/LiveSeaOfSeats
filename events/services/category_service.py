from events.models import Category
from django.utils.text import slugify

def get_or_create_category(api_event):

    classifications = api_event.get("classifications", [])

    if not classifications:
        print("No Category Found")
        return None
    
    classification = classifications[0]

    segment = classification.get("segment", {})

    name = segment.get("name", "Other")
    tm_id = segment.get("id")

    slug = slugify(name)

    category, created = Category.objects.get_or_create(
        slug=slug,
        defaults={
            "name": name,
            "tm_id": tm_id,
            "tm_param": "segmentId",
        }
    )

    if created:
        print(f"Category Created: {name}")
    else:
        print(f"Category Exists: {name}")

    return category