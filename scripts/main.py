from bs4 import BeautifulSoup

repo_url = "git://github.com/Dron3xx-End-to-End/Stiukov.git"


def get_repo_name(repo_url):
    repo_name = repo_url.split("/")[-1].removesuffix(".git")
    return repo_name


def load_portfolio(portfolio):
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
        print("update")
    else:
        print("creating new project")

    return soup


soup = load_portfolio("../aws-cloud-website/index.html")