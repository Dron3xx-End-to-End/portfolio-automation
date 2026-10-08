import sys
from bs4 import BeautifulSoup

from scripts.parse_portfolio_update import parse_portfolio_update

source_file = sys.argv[1]
portfolio = sys.argv[2]
repo_url = sys.argv[3]

data = parse_portfolio_update(source_file)
print(data)

if data["project_name"] == "":
    print("Missing project name in source file")
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


def load_portfolio(portfolio, repo_url):
    with open(portfolio, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    project_items = soup.find_all("li", class_="project-item")

    project_found = False
    project_to_update = None

    repo_name = get_repo_name(repo_url)

    for project in project_items:
        project_link_element = project.find("a", class_="project-link")
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

    return soup


soup = load_portfolio(portfolio, repo_url)