from bs4 import BeautifulSoup, Comment

from creators.html_creator import build_project_html, build_technology_html
from utils.translation_utils import build_translation_key
from utils.html_utils import build_html_indentation

def get_repo_name(repo_url):
    repo_name = repo_url.split("/")[-1].removesuffix(".git")
    return repo_name

def modify_portfolio(portfolio, repo_url, data):
    with open(portfolio, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    project_items = soup.find_all("li", class_="project-item")

    project_found = False
    project_to_update = None

    repo_name = get_repo_name(repo_url)

    repo_name_key = repo_name.replace("-", " ")
    repo_name_key = repo_name_key.title()
    repo_name_key = repo_name_key.replace(" ", "")

    https = (repo_url
             .replace("git://", "https://")
             .removesuffix(".git")
    )

    projects_list = soup.find("ul", class_="projects-list")
    marker = projects_list.find(
        string=lambda text: isinstance(text, Comment)
    )

    full_marker = "<!--" + str(marker) + "-->"
    full_marker_position = content.index(full_marker)

    marker_line_start = content.rfind(
        "\n",
        0,
        full_marker_position
    ) + 1
    marker_indent = content[
        marker_line_start:full_marker_position
    ]

    old_project_key = None
    old_description_key = None

    for project in project_items:
        project_link_element = project.find("a", class_="project-link")

        if project_link_element is None:
            continue

        project_link = (
            project_link_element
            .get("href")
            .split("/")[-1]
            .removesuffix(".git")
        )

        if project_link == repo_name:
            project_found = True
            project_to_update = project
            print("Found project")
            print(f"{project_to_update}")

    if project_found:
        print("updating existing project")
        new_content = content

        project_link_element = project_to_update.find(
            "a", class_="project-link"
        )
        url = project_link_element.get("href")
        url_index = new_content.index(url)
        before_url = new_content[:url_index]

        project_start_index = before_url.rfind(
            '<li class="project-item">'
        )

        project_line_start = new_content.rfind(
            "\n",
            0,
            project_start_index,
        ) + 1

        project_indent = new_content[
            project_line_start:project_start_index
        ]

        indentation = build_html_indentation(project_indent)

        technology_indent = indentation["technology"]

        before_project = new_content[:project_start_index]
        after_project = new_content[url_index:]

        between = new_content[project_start_index:url_index]

        project_name_element = project_to_update.find("h5", class_="project-name")
        old_project_key = project_name_element.get("data-i18n")
        new_project_key = build_translation_key(data["project_name_en"])

        project_description_element = project_to_update.find(
            "p", class_="project-description"
        )
        old_description_key = project_description_element.get("data-i18n")

        project_name = (
            project_to_update
            .find("h5", class_="project-name")
            .get_text(strip=True)
        )
        print(f"Project name: {project_name}")

        if project_name != data["project_name_en"]:
            old_attribute = f'data-i18n="{old_project_key}"'
            new_attribute = f'data-i18n="{new_project_key}"'

            old_description_attribute = f'data-i18n="{old_description_key}"'
            new_description_attribute = f'data-i18n="{new_project_key}Description"'

            project_name_index = between.index(project_name)
            absolute_name_index = project_start_index + project_name_index
            before = new_content[:absolute_name_index] 
            after = new_content[absolute_name_index + len(project_name):]

            change = data["project_name_en"]

            new_content = before + change + after

            url_index = new_content.index(url)
            between = new_content[project_start_index:url_index]
            between = (
            between
            .replace(old_attribute, new_attribute)
            .replace(old_description_attribute, new_description_attribute)
            )

            before_project = new_content[:project_start_index]
            after_project = new_content[url_index:]

            new_content = before_project + between + after_project

        project_description = (
            project_to_update
            .find("p", class_="project-description")
            .get_text(strip=True)
        )
        print(f"Project description: {project_description}")

        if project_description != data["description_en"]:
            project_description_index = between.index(project_description)
            absolute_description_index = (
                project_start_index + project_description_index
            )
            before = new_content[:absolute_description_index] 
            after = new_content[absolute_description_index + len(project_description):]
            change = data["description_en"]

            new_content = before + change + after

            url_index = new_content.index(url)
            between = new_content[project_start_index:url_index]

        project_tech_list = (
            project_to_update
            .find("ul", class_="project-technologies-list")
            .find_all("li")
        )

        technologies = []

        for technology in project_tech_list:
            technology = technology.find_all(string=True, recursive=False)
            technologies.append(technology[0].strip())
        print(f"Project technologies: {technologies}")

        if technologies != data["technologies"]:
            tech_start_tag = '<ul class="project-technologies-list">'
            tech_end_tag = "</ul>"

            absolute_tech_start_index = new_content.index(
                tech_start_tag,
                project_start_index,
            )

            absolute_tech_end_index = new_content.index(
                tech_end_tag,
                absolute_tech_start_index + len(tech_start_tag),
            )

            closing_line_start = new_content.rfind(
                "\n",
                absolute_tech_start_index,
                absolute_tech_end_index,
            ) + 1

            closing_indent = new_content[
                closing_line_start:absolute_tech_end_index
            ]

            before = new_content[:absolute_tech_start_index + len(tech_start_tag)]
            after = new_content[closing_line_start:]

            html_tech_list = build_technology_html(
                data["technologies"],
                technology_indent,
            )

            new_content = (
                before
                + "\n"
                + html_tech_list
                + "\n"
                + after
            )

            url_index = new_content.index(url)
            between = new_content[project_start_index:url_index]

        project_status = (
            project_to_update
            .find("p", class_="project-status")
            .get_text(strip=True)
        )
        print(f"Project status: {project_status}")

        if project_status.removeprefix("Status: ") != data["project_status"]:
            project_status_atr = (
                project_to_update
                .find("p", class_="project-status")
            )
            project_status_key = project_status_atr.get("data-i18n")
            new_status_key = (
                "Status"+
                data["project_status"].title().replace(" ", "")
            )

            status_key_index = between.index(project_status_key)
            absolute_status_key_index = (
                project_start_index + status_key_index
            )

            before = new_content[:absolute_status_key_index]
            after = new_content[absolute_status_key_index+ len(project_status_key):]

            change = new_status_key

            new_content = before + change + after

            url_index = new_content.index(url)
            between = new_content[project_start_index:url_index]

            project_status_index = between.index(project_status)
            absolute_status_index = (
                project_start_index + project_status_index
            )

            before = new_content[:absolute_status_index] 
            after = new_content[absolute_status_index + len(project_status):]

            change = "Status: " + data["project_status"]

            new_content = before + change + after

            url_index = new_content.index(url)
            between = new_content[project_start_index:url_index]

        print(new_content)
        with open(portfolio, "w", encoding="utf-8") as f:
            f.write(new_content)

    else:
        print("creating new project")

        before_marker = content[:marker_line_start]
        after_marker = content[
            marker_line_start:full_marker_position + len(full_marker)
        ]
        after = content[full_marker_position + len(full_marker):]

        print(repr(marker))
        print(f"Marker indent: {repr(marker_indent)}")

        if marker.strip() == "AUTO-GENERATED PROJECTS":

            new_project_html = build_project_html(
                data,
                https,
                marker_indent,
            )

            new_content = (
                before_marker
                + after_marker
                + "\n"
                + new_project_html
                + after
            )

            print(new_content)
            with open(portfolio, "w", encoding="utf-8") as f:
                f.write(new_content)
    return new_content, old_project_key, old_description_key