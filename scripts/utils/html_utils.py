def build_html_indentation(marker_indent):
    child_indent = marker_indent + "    "
    text_indent = child_indent + "    "
    technology_indent = child_indent + "    "

    return {
        "child": child_indent,
        "text": text_indent,
        "technology": technology_indent,
    }
