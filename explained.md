# Portfolio Automation --- Technical Explanation

This document explains the intended responsibilities and data flow of
the Portfolio Automation project. It focuses on how the modules fit
together and why the work is separated into parsing, validation, HTML
handling, and translation handling.

## 1. High-level flow

The automation starts in `main.py` and follows this sequence:

1.  Receive the input Markdown path, portfolio HTML path, repository
    URL, and translation JavaScript path.
2.  Parse the Markdown into a Python dictionary.
3.  Validate the fields required to safely create or update a project.
4.  Pass the structured data to the HTML updater.
5.  Pass the same structured data to the translation updater.
6.  Save the resulting file changes so they can be reviewed and
    committed by the workflow.

The parser converts a human-editable document into structured data. The
update modules can then work with named fields instead of repeatedly
interpreting Markdown.

## 2. Input data and validation

The update document contains:

-   English project name.
-   Polish project name.
-   English description.
-   Polish description.
-   A list of technologies.
-   Project status.

The entry point checks that names and descriptions are not empty, that
at least one technology is provided, and that status is one of the
supported values: `In progress` or `Completed`.

Validation happens before the update functions are called. This helps
prevent incomplete input from being written into the portfolio.

## 3. Why use the repository URL?

The repository URL provides a stable way to identify which project card
should be updated. The HTML updater extracts the repository name from
the URL and compares it with the repository name in each project's
GitHub link.

This is preferable to relying only on the displayed project title: the
title may change, while the repository identity is intended to remain
stable.

The updater also normalizes the URL before writing it to the portfolio,
including removing a trailing `.git` suffix and converting a `git://`
prefix to HTTPS where applicable.

## 4. HTML updater

The HTML updater is responsible for the project cards in the portfolio
page.

### Finding a project

It parses the HTML with Beautiful Soup and searches for list elements
with the `project-item` class. It then examines each project's
`project-link` anchor and compares its repository name with the
repository passed to the script.

### Updating an existing project

When a matching repository is found, the updater compares the current
project data with the new input and updates changed fields, including:

-   English project name.
-   English project description.
-   Technologies list.
-   Project status and the status translation key.

The technology list is rebuilt when its contents differ. Technology
entries can include Devicon icon markup when an icon is configured for
that technology; entries without a configured icon can be rendered as
plain list items.

### Creating a new project

When no matching repository is found, the updater builds a new project
card using the HTML creator. The generated card is inserted at the
designated `AUTO-GENERATED PROJECTS` marker in the portfolio's projects
list.

### Saving the HTML

Both creation and update paths must persist the resulting HTML to the
supplied portfolio file. The returned content alone is not enough:
writing it is what makes the change available to later workflow steps
and to the website repository.

## 5. Translation updater

The translation updater synchronizes the project-related entries in the
JavaScript translation file.

The site uses translation keys in HTML attributes such as `data-i18n`.
The language file maps those keys to their Polish and English text.
Therefore, changing a project title can require changing both the
visible text and the key referenced by the HTML.

A shared key-generation helper normalizes a project name into a key by
title-casing it and removing spaces. The description key is formed by
appending `Description`.

For example, the project name `Portfolio Automation` corresponds to keys
in the shape:

-   `PortfolioAutomation`
-   `PortfolioAutomationDescription`

The updater needs to keep the HTML's `data-i18n` attributes and the
translation entries consistent. When a project name changes, its key
prefix and the corresponding description key prefix must be renamed
consistently. Translation values are updated independently for Polish
and English.

## 6. Creator and updater separation

The `scripts/creators/` modules build the markup or translation entries
needed for a new project. The `scripts/updaters/` modules handle changes
to entries that already exist.

Keeping these responsibilities separate avoids mixing the rules for
creating a complete new project with the logic for finding and
selectively modifying an existing one.

The shared translation utilities keep key-generation rules in one place
so the creator and updater can use the same convention.

## 7. GitHub Actions

The project is intended to run through a GitHub Actions workflow. The
workflow supplies the command-line arguments to `main.py`, allowing the
automation to process the update file and target portfolio files in a
repeatable environment.

A successful local run is useful, but the workflow should also be
checked because its working directory, paths, permissions, and
commit/push steps may differ from a local test.

## 8. Testing checklist

After making changes to the automation, test at least these scenarios:

-   **Create:** use a repository that does not yet have a project card.
-   **Update text:** change the English and Polish names or
    descriptions.
-   **Update technologies:** add, remove, or reorder technologies.
-   **Update status:** switch between `In progress` and `Completed`.
-   **Rename:** change the project name and confirm the HTML translation
    keys and language-file keys remain aligned.
-   **Persistence:** confirm both the HTML file and translation
    JavaScript file contain the changes after execution.
-   **Workflow:** confirm the GitHub Actions run uses the intended
    arguments and has the required repository permissions.

Keep test inputs and output files separate from production files where
possible.

## 9. Known implementation considerations

-   Generated HTML can have different indentation from hand-written
    HTML. Whitespace differences do not necessarily affect browser
    rendering, but readable output makes future debugging and code
    review easier.
-   String-based editing is sensitive to the exact text being searched
    for. If markup or key conventions change, the updater's assumptions
    may need to be updated as well.
-   Translation-key generation can produce collisions if two different
    project names normalize to the same key. If the portfolio grows,
    consider validating key uniqueness.
-   Updating HTML and translations is a multi-file operation. If one
    step fails after another file has been written, the repository may
    be left in a partially updated state. A future improvement would be
    to prepare and validate both outputs before writing either file.

This document describes the intended architecture based on the current
project workflow; keep it aligned with the implementation whenever the
modules or command-line interface change.
