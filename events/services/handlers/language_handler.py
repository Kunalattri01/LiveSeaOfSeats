from events.models import Language


def handle_languages(transformed_data):

    lang_codes = set()

    for row in transformed_data:
        for lang in row.get("languages", []):
            if lang:
                lang_codes.add(lang.strip().lower())

    # 🔥 FIX: use tm_locale instead of code
    existing = Language.objects.filter(tm_locale__in=lang_codes)

    existing_map = {
        l.tm_locale: l
        for l in existing
    }

    to_create = []

    for code in lang_codes:

        if code in existing_map:
            continue

        to_create.append(
            Language(
                name=code.upper(),   # display name
                tm_locale=code
            )
        )

    if to_create:
        Language.objects.bulk_create(
            to_create,
            batch_size=200,
            ignore_conflicts=True
        )

    return {
        l.tm_locale: l
        for l in Language.objects.filter(tm_locale__in=lang_codes)
    }




def attach_languages_to_events(transformed_data, event_map, language_map, source):

    for row in transformed_data:

        event_data = row.get("event_data")
        if not event_data:
            continue

        event_obj = event_map.get((event_data.get("external_id"), source))
        if not event_obj:
            continue

        lang_codes = [
            l.strip().lower()
            for l in row.get("languages", [])
            if l
        ]

        # map to objects
        lang_objs = list(set([
            language_map.get(code)
            for code in lang_codes
            if language_map.get(code)
        ]))

        if not lang_objs:
            continue

        # same as tags (clean & safe)
        event_obj.languages.set(lang_objs)