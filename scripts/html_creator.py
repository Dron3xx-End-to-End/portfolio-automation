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


def build_technology_html(technologies, indent):
    items = []
    inner_indent = indent + "    "

    for tech in technologies:
        if tech in DEVICONS:
            icon = f'<i class="{DEVICONS[tech]}"></i>'
            item = (
                f"{indent}<li>\n"
                f"{inner_indent}{icon}\n"
                f"{inner_indent}{tech}\n"
                f"{indent}</li>"
            )
        else:
            item = f"{indent}<li>{tech}</li>"

        items.append(item)

    return "\n".join(items)


def build_project_html(data, repo_name, repo_url, marker_indent):
    child_indent = marker_indent + "    "
    text_indent = child_indent + "    "

    technologies_html = build_technology_html(
        data["technologies"],
        child_indent + "    ",
    )

    project_html = (
        f'{marker_indent}<li class="project-item">\n'
        f'{child_indent}<h5 class="project-name" '
        f'data-i18n="{repo_name}">\n'
        f'{text_indent}{data["project_name_en"]}\n'
        f'{child_indent}</h5>\n'
        f'\n'
        f'{child_indent}<p class="project-description" '
        f'data-i18n="{repo_name}Description">\n'
        f'{text_indent}{data["description_en"]}\n'
        f'{child_indent}</p>\n'
        f'\n'
        f'{child_indent}<h4 class="project-technologies" '
        f'data-i18n="TechnologiesUsed">\n'
        f'{text_indent}Technologies used:\n'
        f'{child_indent}</h4>\n'
        f'\n'
        f'{child_indent}<ul class="project-technologies-list">\n'
        f'{technologies_html}\n'
        f'{child_indent}</ul>\n'
        f'\n'
        f'{child_indent}<p class="project-status" '
        f'data-i18n="Status{data["project_status"].title().replace(" ", "")}">\n'
        f'{text_indent}Status: {data["project_status"]}\n'
        f'{child_indent}</p>\n'
        f'\n'
        f'{child_indent}<a href="{repo_url}"\n'
        f'{text_indent}target="_blank"\n'
        f'{text_indent}class="btn project-link">\n'
        f'{text_indent}GitHub\n'
        f'{child_indent}</a>\n'
        f'{marker_indent}</li>'
    )

    return project_html