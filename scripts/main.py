import sys

from bs4 import BeautifulSoup, Comment

from scripts.parse_portfolio_update import parse_portfolio_update

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

DEVICONS = {
    "GitHub": "devicon-github-plain colored",
    "Cloud": "devicon-cloud-plain colored",
    "AWS": "devicon-amazonwebservices-plain-wordmark",
    "Docker": "devicon-docker-plain colored",
    "GitHub Actions": "devicon-githubactions-plain colored",
    "Terraform": "devicon-terraform-plain colored",
    "Ansible": "devicon-ansible-plain colored",
    "Python": "devicon-python-plain colored",
    "Bash": "devicon-bash-plain colored",
    "Linux": "devicon-linux-plain colored",
    "Windows": "devicon-windows11-original",
    "HTML": "devicon-html5-plain colored",
    "OpenCV": "devicon-opencv-plain-wordmark colored",
    "TensorFlow": "devicon-tensorflow-original colored",
    "PowerShell": "devicon-powershell-plain colored",
}

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

    ProjectStatus = data["project_status"].title()
    ProjectStatus = ProjectStatus.replace(" ", "")

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
            new_project = soup.new_tag("li")
            new_project["class"] = "project-item"

            new_project_name = soup.new_tag("h5")
            new_project_name["class"] = "project-name"
            new_project_name["data-i18n"] = RepoName
            new_project_name.append("\n\t\t")
            new_project_name.append(data["project_name_en"])
            new_project_name.append("\n\t")

            new_project.append("\n")
            new_project.append("\t")
            new_project.append(new_project_name)

            new_project_description = soup.new_tag("p")
            new_project_description["class"] = "project-description"
            new_project_description["data-i18n"] = (
                RepoName + "Description"
            )
            new_project_description.append("\n\t\t")
            new_project_description.append(data["description_en"])
            new_project_description.append("\n\t")

            new_project.append("\n\n")
            new_project.append("\t")
            new_project.append(new_project_description)

            new_project_tech = soup.new_tag("h4")
            new_project_tech["class"] = "project-technologies"
            new_project_tech["data-i18n"] = "TechnologiesUsed"
            new_project_tech.append("\n\t\t")
            new_project_tech.append("Technologies used:")
            new_project_tech.append("\n\t")

            new_project.append("\n\n")
            new_project.append("\t")
            new_project.append(new_project_tech)

            new_project_tech_list = soup.new_tag("ul")
            new_project_tech_list["class"] = (
                "project-technologies-list"
            )

            for tech in data["technologies"]:
                tech_item = soup.new_tag("li")
                tech_item.append("\n\t\t")

                if tech in DEVICONS:
                    tech_item_devicon = soup.new_tag("i")
                    tech_item_devicon["class"] = DEVICONS[tech]
                    tech_item.append(tech_item_devicon)
                    tech_item.append("\n\t\t")

                tech_item.append(tech)
                tech_item.append("\n\t")

                new_project_tech_list.append("\n\n\t")
                new_project_tech_list.append(tech_item)

            new_project_tech_list.append("\n")

            new_project.append("\n\n")
            new_project.append("\t")
            new_project.append(new_project_tech_list)

            new_project_status = soup.new_tag("p")
            new_project_status["class"] = "project-status"
            new_project_status["data-i18n"] = (
                "Status" + ProjectStatus
            )
            new_project_status.append("\n\t\t")
            new_project_status.append(
                "Status: " + data["project_status"]
            )
            new_project_status.append("\n\t")

            new_project.append("\n\n")
            new_project.append("\t")
            new_project.append(new_project_status)

            new_project_link = soup.new_tag("a")
            new_project_link["href"] = https
            new_project_link["target"] = "_blank"
            new_project_link["class"] = "btn project-link"
            new_project_link.append("\n\t\t")
            new_project_link.append("GitHub")
            new_project_link.append("\n\t")

            new_project.append("\n\n")
            new_project.append("\t")
            new_project.append(new_project_link)

            new_project.append("\n\n")

            new_project_html = str(new_project)

            new_project_html = (
                marker_indent
                + new_project_html.replace(
                    "\n",
                    "\n" + marker_indent
                )
            )

            new_content = (
                before_marker
                + new_project_html
                + after_marker
            )
            new_project_html += "\n"

            print(new_content)
    return soup


soup = modify_portfolio(portfolio, repo_url)