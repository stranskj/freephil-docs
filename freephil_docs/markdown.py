from freephil import parse


def generate_phil_markdown(master_scope, title="PHIL Parameters Documentation", description=None,
                           default_scope_description=True):
    """
    Generates a Markdown string from a master PHIL scope.

    Args:
        master_scope: A parsed PHIL object representing the master scope.
        title (str): Title of the Markdown document.
        description (str): A general description to appear at the top of the document.
        default_scope_description (bool): Whether to include a default description for scopes without a `.help`.

    Returns:
        str: A Markdown-formatted string documenting the PHIL parameters.
    """
    markdown = [f"# {title}\n"]

    # Add general description if provided
    if description:
        markdown.append(f"{description}\n\n")

    # Helper function to generate the hierarchical structure for the overview
    def generate_overview(scope, prefix=""):
        overview = []
        for obj in scope.objects:
            full_name = f"{prefix}.{obj.name}" if prefix else obj.name
            if obj.is_scope:
                overview.append(f"- {full_name}/")
                overview.extend(generate_overview(obj, full_name))
            elif obj.is_definition:
                overview.append(f"- [{full_name}](#{full_name.replace('.', '-').lower()})")
        return overview

    # Generate the overview
    markdown.append("## Overview\n")
    markdown.extend(generate_overview(master_scope))
    markdown.append("\n")

    # Helper function to describe each parameter
    def describe_scope(scope, prefix=""):
        for obj in scope.objects:
            full_name = f"{prefix}.{obj.name}" if prefix else obj.name
            if obj.is_scope:
                markdown.append(f"### {full_name}/\n")
                if obj.help:
                    markdown.append(f"{obj.help}\n\n")
                elif default_scope_description:
                    markdown.append("*This is a scope containing sub-parameters.*\n\n")
                describe_scope(obj, full_name)
            elif obj.is_definition:
                markdown.append(f"### {full_name}\n")
                markdown.append(f"- **Type**: {obj.type.name}\n")
                if obj.default is not None:
                    markdown.append(f"- **Default**: `{obj.default}`\n")
                if obj.help:
                    markdown.append(f"{obj.help}\n\n")
                else:
                    markdown.append("\n")

    # Generate detailed descriptions
    markdown.append("## Parameter Descriptions\n")
    describe_scope(master_scope)

    # Return as a single string
    return "\n".join(markdown)


# Example usage
phil_content = """
scope_1 {
    param_1 = 10
        .type = int
        .help = "An integer parameter used for calculations."
    scope_2 {
        .help = "This scope contains string parameters for configuration."
        param_2 = "default"
            .type = str
            .help = "A string parameter specifying the mode of operation."
    }
    scope_3 {
        param_3 = 42
            .type = int
    }
}
"""

# Parse the PHIL content
master_scope = parse(phil_content)

# Generate Markdown with default scope descriptions enabled
markdown_output = generate_phil_markdown(
    master_scope,
    title="Custom PHIL Documentation",
    description="This document provides a structured overview of PHIL parameters.",
    default_scope_description=True
)

print(markdown_output)  # To preview the output
