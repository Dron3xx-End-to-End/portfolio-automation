import sys

from bs4 import BeautifulSoup, Comment

from scripts.parse_portfolio_update import parse_portfolio_update
from scripts.html_creator import build_project_html

source_file = sys.argv[1]
portfolio = sys.argv[2]
repo_url = sys.argv[3]

data = parse_portfolio_update(source_file)
print(data)

if data["project_name_en"] == "":
    print("Missing english project name in source file")
    sys.exit(1)
elif data["project_name_pl"] == "":
    print("Missing polish project name in source file")
    sys.exit(1)
elif data["technologies"] == []:
    print("Missing technologies in source file")
    sys.exit(1)
elif data["description_en"] == "":
    print("Missing description_en in source file")
    sys.exit(1)
elif data["description_pl"] == "":
    print("Missing description_pl in source file")
    sys.exit(1)


def get_repo_name(repo_url):
    repo_name = repo_url.split("/")[-1].removesuffix(".git")
    return repo_name


def modify_portfolio(portfolio, repo_url):
    with open(portfolio, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    project_items = soup.find_all("li", class_="project-item")

    project_found = False
    project_to_update = None

    repo_name = get_repo_name(repo_url)

    RepoName = repo_name.replace("-", " ")
    RepoName = RepoName.title()
    RepoName = RepoName.replace(" ", "")

    https = (repo_url
             .replace("git://", "https://")
             .removesuffix(".git")
    )

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

        project_name = (
            project_to_update
            .find("h5", class_="project-name")
            .get_text(strip=True)
        )
        print(f"Project name: {project_name}")

        project_description = (
            project_to_update
            .find("p", class_="project-description")
            .get_text(strip=True)
        )
        print(f"Project description: {project_description}")

        project_tech_list = (
            project_to_update
            .find("ul", class_="project-technologies-list")
            .find_all("li")
        )

        technologies = []

        for technology in project_tech_list:
            technologies.append(technology.get_text(strip=True))
        print(f"Project technologies: {technologies}")

        project_status = (
            project_to_update
            .find("p", class_="project-status")
            .get_text(strip=True)
        )
        print(f"Project status: {project_status}")
        print("update")

    else:
        print("creating new project")

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
        before_marker = content[:marker_line_start]
        after_marker = content[marker_line_start:]
        marker_indent = content[
            marker_line_start:full_marker_position
        ]

        print(repr(marker))
        print(f"Marker indent: {repr(marker_indent)}")

        if marker.strip() == "AUTO-GENERATED PROJECTS":

            new_project_html = build_project_html(
                data,
                RepoName,
                https,
                marker_indent,
            )

            new_content = (
                before_marker
                + new_project_html
                + "\n"
                + after_marker
            )
            print(new_content)
            print(repr(marker_indent))
    return soup


soup = modify_portfolio(portfolio, repo_url)