from organizer.models import Organizer

def get_or_create_organizer(api_event):

    attractions = api_event.get("_embedded", {}).get("attractions", [])

    if not attractions:
        print("❌ No Organizer Found")
        return None

    attraction = attractions[0]

    organizer_name = attraction.get("name", "Unknown Organizer")
    email = "external@example.com"
    phone = "0000000000"

    external_links = attraction.get("externalLinks", {})

    website = attraction.get("url", "")
    instagram = ""
    twitter = ""
    facebook = ""

    if "homepage" in external_links:
        website = external_links["homepage"][0].get("url", "")

    if "instagram" in external_links:
        instagram = external_links["instagram"][0].get("url", "")

    if "facebook" in external_links:
        facebook = external_links["facebook"][0].get("url", "")

    if "twitter" in external_links:
        twitter = external_links["twitter"][0].get("url", "")


    organizer, created = Organizer.objects.get_or_create(
        name = organizer_name,
        defaults={
            "email": email,
            "phone": phone,
            "website": website,
            "instagram": instagram,
            "facebook": facebook,
            "twitter": twitter,
        }
    )

    if created:
        print(f"Organizer Created: {organizer_name}")
    else:
        print(f"Organizer Exists: {organizer_name}")
        

    return organizer