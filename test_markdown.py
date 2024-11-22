from freephil import parse
from freephil_docs.markdown import generate_phil_markdown

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