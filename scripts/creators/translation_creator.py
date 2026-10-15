from utils.translation_utils import build_translation_key

def translation(data):
    project_key = build_translation_key(data["project_name_en"])
    description_project_key = project_key + "Description"

    pl_translations = {
        project_key: data["project_name_pl"],
        description_project_key: data["description_pl"]
    }
    eng_translations = {
        project_key: data["project_name_en"],
        description_project_key: data["description_en"],
    }
    return pl_translations, eng_translations