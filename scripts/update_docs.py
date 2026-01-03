import re
import subprocess
from pathlib import Path


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
    header_level = len(re.match(r"^#+", lines[start_idx]).group())

    section_lines = [lines[start_idx]]
    for line in lines[start_idx + 1 :]:
        match = re.match(r"^(#+)", line)
        if match and len(match.group()) <= header_level:
            break
        section_lines.append(line)

    return "\n".join(section_lines)


def main():
    root = Path(__file__).parent.parent
    docs_dir = root / "docs"

    # Generate full API docs template
    full_docs = get_api_docs("focusnfe.client")
    model_nfse_docs = get_api_docs("focusnfe.models.nfse")
    model_nfe_docs = get_api_docs("focusnfe.models.nfe")

    # --- Update NF-e Docs ---
    nfe_content = []
    nfe_content.append("### Client Methods\n")
    nfe_content.append(extract_section(full_docs, "#### create\\_nfe"))
    nfe_content.append(extract_section(full_docs, "#### get\\_nfe"))
    nfe_content.append(extract_section(full_docs, "#### cancel\\_nfe"))
    nfe_content.append("\n### Models\n")
    nfe_content.append(extract_section(model_nfe_docs, "## NFeResponse Objects"))

    update_file(docs_dir / "nfe.md", "\n\n".join(nfe_content))

    # --- Update NFS-e Docs ---
    nfse_content = []
    nfse_content.append("### Client Methods\n")
    nfse_content.append(extract_section(full_docs, "#### create\\_nfse"))
    nfse_content.append(extract_section(full_docs, "#### get\\_nfse"))
    nfse_content.append(extract_section(full_docs, "#### cancel\\_nfse"))
    nfse_content.append("\n### Models\n")
    nfse_content.append(extract_section(model_nfse_docs, "## NFSeRequest Objects"))
    nfse_content.append(extract_section(model_nfse_docs, "## NFSeResponse Objects"))
    nfse_content.append(extract_section(model_nfse_docs, "## NFSePrestador Objects"))
    nfse_content.append(extract_section(model_nfse_docs, "## NFSeTomador Objects"))
    nfse_content.append(extract_section(model_nfse_docs, "## NFSeTomadorEndereco Objects"))
    nfse_content.append(extract_section(model_nfse_docs, "## NFSeServico Objects"))

    update_file(docs_dir / "nfse.md", "\n\n".join(nfse_content))


if __name__ == "__main__":
    main()
