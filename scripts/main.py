import sys

from parse_portfolio_update import parse_portfolio_update
from updaters.html_updater import modify_portfolio
from updaters.translation_updater import modify_language

source_file = sys.argv[1]
portfolio = sys.argv[2]
repo_url = sys.argv[3]
language = sys.argv[4]

data = parse_portfolio_update(source_file)
print(data)
STATUS = [
    "In progress",
    "Completed",
]

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
elif data["project_status"] == "":
    print("Missing project_status in source file")
    sys.exit(1)
elif data["project_status"] not in STATUS:
    print("Non acceptable project_status")
    sys.exit(1)

(
    new_content,
    old_project_key,
    old_description_key,
) = modify_portfolio(portfolio, repo_url, data)

new_translation = modify_language(
    data,
    language,
    old_project_key,
    old_description_key,
)