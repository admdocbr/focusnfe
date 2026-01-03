import re
import subprocess
import sys
from pathlib import Path

# Add src to path so we can import models
root = Path(__file__).parent.parent
sys.path.append(str(root / "src"))

from focusnfe.models.nfe import NFeResponse  # noqa: E402
from focusnfe.models.nfse import (  # noqa: E402
    NFSePrestador,
    NFSeRequest,
    NFSeResponse,
    NFSeServico,
    NFSeTomador,
    NFSeTomadorEndereco,
)


def get_api_docs(module_name):
    """Run pydoc-markdown and return the output."""
    result = subprocess.run(
        ["pydoc-markdown", "-m", module_name, "--render-toc"], capture_output=True, text=True, check=True
    )
    return result.stdout


def update_file(file_path, new_content):
    """Update content between API_DOCS markers in a file."""
    content = file_path.read_text()

    start_marker = "<!-- API_DOCS_START -->"
    end_marker = "<!-- API_DOCS_END -->"

    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)

    if not pattern.search(content):
        print(f"Markers not found in {file_path}")
        return False

    replacement = f"{start_marker}\n\n{new_content.strip()}\n\n{end_marker}"
    new_text = pattern.sub(replacement, content)

    file_path.write_text(new_text)
    print(f"Updated {file_path}")
    return True


def extract_section(markdown, header):
    """Extract a section from markdown based on a header."""
    lines = markdown.splitlines()
    start_idx = -1
    for i, line in enumerate(lines):
        if header in line:
            start_idx = i
            break

    if start_idx == -1:
        return ""

    # Find next header of same or higher level
    match = re.match(r"^#+", lines[start_idx])
    if not match:
        # Not a valid markdown header line
        return ""
    header_level = len(match.group())

    section_lines = [lines[start_idx]]
    for line in lines[start_idx + 1 :]:
        match = re.match(r"^(#+)", line)
        if match and len(match.group()) <= header_level:
            break
        section_lines.append(line)

    return "\n".join(section_lines)


def get_model_docs(model_class):
    """Generate markdown documentation for a Pydantic model including its fields."""
    name = model_class.__name__
    doc = model_class.__doc__ or ""

    lines = [f"#### `{name}`", f"{doc.strip()}\n"]
    lines.append("| Field | Type | Description |")
    lines.append("| :--- | :--- | :--- |")

    for field_name, field in model_class.model_fields.items():
        # Get simplified type name
        annotation = field.annotation
        type_hint = str(annotation).replace("typing.", "").replace("NoneType", "None")

        # Handle Union types (like str | None)
        type_hint = type_hint.replace("Union[", "").replace("]", "").replace(", ", " | ")

        # Handle basic classes
        if "<class '" in type_hint:
            type_hint = type_hint.split("'")[1].split(".")[-1]

        if "focusnfe.models" in type_hint:
            type_hint = type_hint.split(".")[-1]

        description = field.description or "-"
        # Escape pipes in type hints to prevent markdown table column issues
        type_cell = type_hint.replace("|", "\\|")
        lines.append(f"| `{field_name}` | `{type_cell}` | {description} |")

    return "\n".join(lines)


def main():
    docs_dir = root / "docs"

    # Generate full API docs template
    full_docs = get_api_docs("focusnfe.client")

    # --- Update NF-e Docs ---
    nfe_content = []
    nfe_content.append("### Client Methods\n")
    nfe_content.append(extract_section(full_docs, "#### create\\_nfe"))
    nfe_content.append(extract_section(full_docs, "#### get\\_nfe"))
    nfe_content.append(extract_section(full_docs, "#### cancel\\_nfe"))
    nfe_content.append("\n### Models\n")
    nfe_content.append(get_model_docs(NFeResponse))

    update_file(docs_dir / "nfe.md", "\n\n".join(nfe_content))

    # --- Update NFS-e Docs ---
    nfse_content = []
    nfse_content.append("### Client Methods\n")
    nfse_content.append(extract_section(full_docs, "#### create\\_nfse"))
    nfse_content.append(extract_section(full_docs, "#### get\\_nfse"))
    nfse_content.append(extract_section(full_docs, "#### cancel\\_nfse"))
    nfse_content.append("\n### Models\n")
    nfse_content.append(get_model_docs(NFSeRequest))
    nfse_content.append(get_model_docs(NFSeResponse))
    nfse_content.append(get_model_docs(NFSePrestador))
    nfse_content.append(get_model_docs(NFSeTomador))
    nfse_content.append(get_model_docs(NFSeTomadorEndereco))
    nfse_content.append(get_model_docs(NFSeServico))

    update_file(docs_dir / "nfse.md", "\n\n".join(nfse_content))


if __name__ == "__main__":
    main()
