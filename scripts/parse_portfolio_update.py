def parse_portfolio_update(source_file):
    data = {
        "project_name_en": "",
        "project_name_pl": "",
        "description_en": "",
        "description_pl": "",
        "technologies": [],
        "project_status": "",
    }

    section = None
    under_section = None
    with open(source_file, 'r', encoding='utf-8') as f:
        for line in f:
            strip_line = line.strip()

            if not strip_line:
                continue

            if strip_line.startswith("## "):
                section = strip_line.replace("## ", "").lower()
            
            elif strip_line.startswith("### "):
                under_section = strip_line.replace("### ", "").lower()

            else:
                if section == "project name" and under_section == "english":
                    data["project_name_en"] = strip_line

                elif section == "project name" and under_section == "polski":
                    data["project_name_pl"] = strip_line

                elif section == "technologies":
                    data["technologies"].append(strip_line.strip("- "))

                elif section == "description" and under_section == "english":
                    data["description_en"] = strip_line

                elif section == "description" and under_section == "polski":
                    data["description_pl"] = strip_line

                elif section == "status":
                    data["project_status"] = strip_line

    return data
