from organizer.models import Organizer

ORGANIZER_CACHE = {}

def get_or_create_organizer(api_event):

    attractions = api_event.get("_embedded", {}).get("attractions", [])

    if not attractions:
        return None

    attraction = attractions[0]

    organizer_name = attraction.get("name", "Unknown Organizer")
    tm_id = attraction.get("id")   # ✅ IMPORTANT

    # ✅ 1. Check cache first (BIG SPEED BOOST)
    if tm_id in ORGANIZER_CACHE:
        return ORGANIZER_CACHE[tm_id]

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

    # ✅ 2. Use update_or_create with tm_id (correct uniqueness)
    organizer, _ = Organizer.objects.update_or_create(
        tm_id=tm_id,
        defaults={
            "name": organizer_name,
            "email": email,
            "phone": phone,
            "website": website,
            "instagram": instagram,
            "facebook": facebook,
            "twitter": twitter,
        }
    )

    # ✅ 3. Store in cache
    ORGANIZER_CACHE[tm_id] = organizer

    return organizer















































# from organizer.models import Organizer

# def get_or_create_organizer(api_event):

#     attractions = api_event.get("_embedded", {}).get("attractions", [])

#     if not attractions:
#         return None

#     attraction = attractions[0]

#     organizer_name = attraction.get("name", "Unknown Organizer")
#     email = "external@example.com"
#     phone = "0000000000"

#     external_links = attraction.get("externalLinks", {})

#     website = attraction.get("url", "")
#     instagram = ""
#     twitter = ""
#     facebook = ""

#     if "homepage" in external_links:
#         website = external_links["homepage"][0].get("url", "")

#     if "instagram" in external_links:
#         instagram = external_links["instagram"][0].get("url", "")

#     if "facebook" in external_links:
#         facebook = external_links["facebook"][0].get("url", "")

#     if "twitter" in external_links:
#         twitter = external_links["twitter"][0].get("url", "")


#     organizer, created = Organizer.objects.get_or_create(
#         name = organizer_name,
#         defaults={
#             "email": email,
#             "phone": phone,
#             "website": website,
#             "instagram": instagram,
#             "facebook": facebook,
#             "twitter": twitter,
#         }
#     )      

#     return organizer