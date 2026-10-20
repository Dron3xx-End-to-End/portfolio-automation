from creators.translation_creator import translation

def modify_language(data, language, old_project_key, old_description_key):
    pl_translations, eng_translations = translation(data)

    with open(language, "r", encoding="utf-8") as f:
        content = f.read()

    new_translation_content = content

    pl_marker = "// AUTO-GENERATED PL TRANSLATIONS"
    pl_index = new_translation_content.rfind(
        pl_marker
    )
    before_pl_index = new_translation_content[:pl_index]
    after_pl = new_translation_content[pl_index + len(pl_marker):]
    change_pl = ""

    eng_marker = "// AUTO-GENERATED ENG TRANSLATIONS"
    eng_index = new_translation_content.rfind(
        eng_marker
    )
    before_eng_index = new_translation_content[:eng_index]
    after_eng = new_translation_content[eng_index + len(eng_marker):]
    change_eng = ""

    if (
        (old_project_key is None and old_description_key is None)
        or
        (
            old_project_key not in new_translation_content
            and old_description_key not in new_translation_content
        )
    ):
        print("Creating new translations")
        for key, value in pl_translations.items():
            change_pl += f'\t\t{key}: "{value}",\n'

        new_translation_content = (
            before_pl_index
            + pl_marker
            + "\n\n"
            + change_pl
            + after_pl
        )

        eng_index = new_translation_content.rfind(
            eng_marker
        )
        before_eng_index = new_translation_content[:eng_index]
        after_eng = new_translation_content[eng_index + len(eng_marker):]

        for key, value in eng_translations.items():
            change_eng += f'\t\t{key}: "{value}",\n'

        new_translation_content = (
            before_eng_index
            + eng_marker
            + "\n\n"
            + change_eng
            + after_eng
        )
        
        print(new_translation_content)
        with open(language, "w", encoding="utf-8") as f:
            f.write(new_translation_content)
    else:
        print("Updating existing translations")

        keys_list = list(pl_translations.keys())
        project_key = keys_list[0]
        description_key = keys_list[1]


        start_pl_marker = "// START PL TRANSLATIONS"
        end_pl_marker = "// END PL TRANSLATIONS"

        start_pl_content = new_translation_content.rfind(
            start_pl_marker
        ) + len(start_pl_marker)
        end_pl_content = new_translation_content.rfind(
            end_pl_marker
        )

        before_pl = new_translation_content[:start_pl_content]
        after_pl = new_translation_content[end_pl_content:]

        pl_section = new_translation_content[start_pl_content:end_pl_content]

        pl_project_key_end = pl_section.find(old_project_key) + len(old_project_key)
        pl_project_key_end = pl_section.find(":", pl_project_key_end)

        pl_project_value_start = pl_section.find('"', pl_project_key_end)
        pl_project_value_end = pl_section.find('"', pl_project_value_start + 1)

        pl_project_value_fragment = pl_section[pl_project_value_start + 1:pl_project_value_end]

        pl_description_key_end = pl_section.find(old_description_key) + len(old_description_key)
        pl_description_key_end = pl_section.find(":", pl_description_key_end)

        pl_description_value_start = pl_section.find('"', pl_description_key_end)
        pl_description_value_end = pl_section.find('"', pl_description_value_start + 1)

        pl_description_value_fragment = pl_section[pl_description_value_start + 1:pl_description_value_end]

        start_eng_marker = "// START ENG TRANSLATIONS"
        end_eng_marker = "// END ENG TRANSLATIONS"

        start_eng_content = new_translation_content.rfind(
            start_eng_marker
        ) + len(start_eng_marker)
        end_eng_content = new_translation_content.rfind(
            end_eng_marker
        )

        before_eng = new_translation_content[:start_eng_content]
        after_eng = new_translation_content[end_eng_content:]

        eng_section = new_translation_content[start_eng_content:end_eng_content]

        eng_project_key_end = eng_section.find(old_project_key) + len(old_project_key)
        eng_project_key_end = eng_section.find(":", eng_project_key_end)

        eng_project_value_start = eng_section.find('"', eng_project_key_end)
        eng_project_value_end = eng_section.find('"', eng_project_value_start + 1)

        eng_project_value_fragment = eng_section[eng_project_value_start + 1:eng_project_value_end]

        eng_description_key_end = eng_section.find(old_description_key) + len(old_description_key)
        eng_description_key_end = eng_section.find(":", eng_description_key_end)

        eng_description_value_start = eng_section.find('"', eng_description_key_end)
        eng_description_value_end = eng_section.find('"', eng_description_value_start + 1)

        eng_description_value_fragment = eng_section[eng_description_value_start + 1:eng_description_value_end]

        if pl_translations[project_key] != pl_project_value_fragment:
            pl_section = pl_section.replace(
                pl_project_value_fragment, pl_translations[project_key]
                )

        if pl_translations[description_key] != pl_description_value_fragment:
            pl_section = pl_section.replace(
                pl_description_value_fragment, pl_translations[description_key]
            )

        new_translation_content = before_pl + pl_section + after_pl

        start_eng_content = new_translation_content.rfind(
            start_eng_marker
        ) + len(start_eng_marker)
        end_eng_content = new_translation_content.rfind(
            end_eng_marker
        )

        before_eng = new_translation_content[:start_eng_content]
        after_eng = new_translation_content[end_eng_content:]

        eng_section = new_translation_content[start_eng_content:end_eng_content]

        if eng_translations[project_key] != eng_project_value_fragment:
            eng_section = eng_section.replace(
                eng_project_value_fragment, eng_translations[project_key]
                )

        if eng_translations[description_key] != eng_description_value_fragment:
            eng_section = eng_section.replace(
                eng_description_value_fragment, eng_translations[description_key]
            )

        new_translation_content = before_eng + eng_section + after_eng

        if project_key != old_project_key:
            new_translation_content = new_translation_content.replace(
                old_project_key, project_key
            )

        with open(language, "w", encoding="utf-8") as f:
            f.write(new_translation_content)

    print("New translation content: ", new_translation_content)
    return new_translation_content
