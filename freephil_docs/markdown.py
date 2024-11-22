
def phil_to_markdown(master_scope, title="PHIL Parameters Documentation", description=None, default_scope_description=True):
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
        markdown.append(f"{description}\n")

    # Helper function to generate the hierarchical structure for the overview
    def generate_overview(scope, prefix="", offset=''):
        overview = []
        for obj in scope.objects:
            if obj.is_scope:
                # Indented scope link in the overview
                overview.append \
                    (f"{offset}- [{obj.name}]({prefix + '.' + obj.name if prefix else obj.name})/")
                # Recursively generate overview for nested scopes
                overview.extend \
                    (generate_overview(obj, prefix + '.' + obj.name if prefix else obj.name, offset= f'  {offset}'))
            elif obj.is_definition:
                # Indented parameter link in the overview
                overview.append \
                    (f"{offset}- [{obj.name}](#{(prefix + '.' + obj.name if prefix else obj.name).replace('.', '-').lower()})")
        return overview

    # Generate the overview
    markdown.append("## Overview\n")
    markdown.extend(generate_overview(master_scope))
    markdown.append("\n")

    # Helper function to describe each parameter and scope
    def describe_scope(scope, prefix=""):
        for obj in scope.objects:
            full_name = f"{prefix}.{obj.name}" if prefix else obj.name
            if obj.is_scope:
                markdown.append(f"### {full_name}/\n")
                if obj.help:
                    markdown.append(f"{obj.help}\n\n")
                elif default_scope_description:
                    markdown.append("*This is a scope containing sub-parameters.*\n\n")
                describe_scope(obj, full_name)  # Recursive call to handle nested scopes
            elif obj.is_definition:
                markdown.append(f"### {full_name}\n")
                markdown.append(f"- **Type**: {obj.type.phil_type}")
                if obj.words:
                    words = ' '.join([wrd.value for wrd in obj.words])
                    markdown.append(f"- **Default**: `{words}`")
                if obj.multiple:
                    markdown.append("- **Multiple**: Yes")
                else:
                    markdown.append("- **Multiple**: No")
                if obj.help:
                    markdown.append(f"\n{obj.help}\n")
                else:
                    markdown.append("")

    # Generate detailed descriptions
    markdown.append("## Parameter Descriptions\n")
    describe_scope(master_scope)

    # Return as a single string
    return "\n".join(markdown)


