from scripts.creators.translation_creator import translation

def modify_language(data, language, old_project_key, old_description_key):
    pl_translations, eng_translations = translation(data)

    with open(language, "r", encoding="utf-8") as f:
        content = f.read()

    new_translation_content = content

    pl_index = new_translation_content.rfind(
        "// AUTO-GENERATED PL TRANSLATIONS"
    )
    before_pl = new_translation_content[:pl_index]
    after_pl = new_translation_content[pl_index:]
    change_pl = ""
    for key, value in pl_translations.items():
        change_pl += f'{key}: "{value}",\n'

    new_translation_content = before_pl + change_pl + after_pl

    eng_index = new_translation_content.rfind(
        "// AUTO-GENERATED ENG TRANSLATIONS"
    )
    before_eng = new_translation_content[:eng_index]
    after_eng = new_translation_content[eng_index:]
    change_eng = ""
    for key, value in eng_translations.items():
        change_eng += f'{key}: "{value}",\n'

    new_translation_content = before_eng + change_eng + after_eng

    pl_content = new_translation_content[pl_index:eng_index]
    eng_content = new_translation_content[eng_index:]

    translation_found = False
    translation_to_update = None

    if old_project_key in new_translation_content:
        translation_found = True
    elif old_description_key in new_translation_content:
        translation_found = True

    if translation_found:


    return new_translation_content
