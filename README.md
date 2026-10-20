# Portfolio Automation

A Python automation project that processes structured portfolio updates
and synchronizes project information with a portfolio website.

The project is designed to reduce the need to manually edit project
cards in the website's HTML and maintain matching Polish and English
translations.

## Features

-   Reads project information from a Markdown update file.
-   Validates required project fields and the project status.
-   Creates a project card when the repository is not already
    represented in the portfolio.
-   Updates an existing project card when the repository is already
    present.
-   Updates project names, descriptions, technologies, and status in the
    HTML.
-   Synchronizes project translation keys and values in the language
    JavaScript file.
-   Uses the repository URL to identify the project and construct its
    GitHub link.

## Technologies

-   **Python** --- automation logic and file processing.
-   **Beautiful Soup** --- parsing the portfolio HTML to locate project
    elements.
-   **GitHub Actions** --- running the automation as part of a workflow.
-   **GitHub API / GitHub repository workflow** --- project context and
    repository-based automation.

## Project update format

The automation reads a Markdown file with sections for the project name,
description, technologies, and status. Names and descriptions are
provided in English and Polish.

Example:

``` markdown
# Portfolio Update

## Project Name

### English

Portfolio Automation

### Polski

Automatyzacja Portfolio

## Description

### English

GitHub Actions automation for automatically processing project updates and synchronizing them with a Cloud & DevOps portfolio.

### Polski

Automatyzacja GitHub Actions do przetwarzania aktualizacji projektów i synchronizacji ich z portfolio Cloud & DevOps.

## Technologies

- GitHub Actions
- GitHub API
- Python

## Status

In progress
```

The accepted status values in the current implementation are:

-   `In progress`
-   `Completed`

The project names, both descriptions, technologies, and status must be
present. The program exits with an error if a required field is missing
or the status is not accepted.

## Running the script

The entry point is `main.py`. In the workflow version, it receives four
command-line arguments:

``` bash
python main.py <source_file> <portfolio_html> <repository_url> <language_file>
```

Arguments:

1.  `source_file` --- path to the Markdown update file.
2.  `portfolio_html` --- path to the portfolio HTML file, for example
    `index.html`.
3.  `repository_url` --- URL of the repository represented by the
    project card.
4.  `language_file` --- path to the JavaScript file containing
    translations, for example `js/language.js`.

Example shape (replace paths and URL with the values for your
environment):

``` bash
python main.py portfolio-update.md index.html https://github.com/OWNER/REPOSITORY js/language.js
```

Run the command from the project root and ensure the Python dependencies
are installed. The exact dependency installation command should match
the dependency file in the repository.

## Processing flow

1.  `main.py` reads the command-line arguments.
2.  `parse_portfolio_update.py` parses the Markdown update into
    structured data.
3.  `main.py` validates required fields and the status.
4.  The HTML updater creates or updates the matching project card.
5.  The translation updater synchronizes the relevant translation
    entries.
6.  The updated files can then be reviewed and committed by the
    repository workflow.

## Repository structure

The project is organized by responsibility:

-   `main.py` --- command-line entry point and orchestration.
-   `scripts/parse_portfolio_update.py` --- reads the Markdown update
    file.
-   `scripts/creators/` --- builds HTML and translation content for new
    projects.
-   `scripts/updaters/` --- updates existing portfolio HTML and
    translation content.
-   `utils/translation_utils.py` --- shared translation-key helpers.
-   `portfolio-update.md` --- example input describing a project update.
-   GitHub Actions workflow files --- automate execution in the
    repository workflow.

File names and exact implementation details may evolve as the project
develops.

## Notes

-   Back up or commit the portfolio files before testing updates.
-   Test both cases: adding a new repository and updating a repository
    already in the portfolio.
-   After a run, check both the HTML project card and its Polish/English
    translation entries.
-   HTML whitespace may differ from hand-formatted markup even when the
    resulting page renders correctly.
