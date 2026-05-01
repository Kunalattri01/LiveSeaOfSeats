from events.models import Event, Language


def sync_languages(api_events):

    for api_event in api_events:

        locale = api_event.get("locale")

        if not locale:
            continue

        lang, _ = Language.objects.get_or_create(
            tm_locale=locale.lower(),
            defaults={"name": locale.upper()}
        )

        for event in Event.objects.all():
            event.languages.add(lang)