"""Markdown section parser for book research files and checklists."""

from __future__ import annotations

import re
from pathlib import Path


# Section heading patterns in book research files
SECTION_PATTERNS = {
    "key_ideas": r"(?:Key Ideas|Mental Models|Core Thesis|Core Insight|Core Pattern|Core Principle|Core Problem|Core Finding|Core Innovation|Core Technique|General Principles|Overview|What |Note\b|Original Key Points)",
    "patterns": r"(?:Patterns|Approaches|Design Principles|Architecture|Workflow|The \d+ )",
    "tradeoffs": r"(?:Tradeoffs|Tensions|Challenges|Limitations|Production Challenges)",
    "pitfalls": r"(?:Watch Out|What to Watch|Pitfalls|Anti-Pattern|Architectural Limitations)",
    "applicability": r"(?:Applicability)",
    "framings": r"(?:Key Framings|Framings Worth Preserving|Key Quotable|Key Quotables|Key Insight)",
}


def extract_section(content: str, section: str) -> str | None:
    """Extract a named section from a markdown file.

    Looks for a ## heading matching the section pattern and returns all content
    until the next ## heading or end of file.
    """
    if section == "full":
        return content

    pattern = SECTION_PATTERNS.get(section)
    if not pattern:
        return None

    # Find the heading
    heading_re = re.compile(
        rf"^##\s+.*{pattern}.*$", re.MULTILINE | re.IGNORECASE
    )
    match = heading_re.search(content)
    if not match:
        return None

    start = match.start()

    # Find the next ## heading after this one
    next_heading = re.search(r"^##\s+", content[match.end() :], re.MULTILINE)
    if next_heading:
        end = match.end() + next_heading.start()
    else:
        end = len(content)

    return content[start:end].strip()


def extract_checklist_section(content: str, section_name: str) -> str | None:
    """Extract a named section from a checklist file.

    Looks for ## headings and returns the matching section content.
    """
    heading_re = re.compile(
        rf"^##\s+.*{re.escape(section_name)}.*$", re.MULTILINE | re.IGNORECASE
    )
    match = heading_re.search(content)
    if not match:
        return None

    start = match.start()
    next_heading = re.search(r"^##\s+", content[match.end() :], re.MULTILINE)
    if next_heading:
        end = match.end() + next_heading.start()
    else:
        end = len(content)

    return content[start:end].strip()


def extract_items_only(content: str) -> str:
    """Extract only checklist items (lines starting with '- [ ]') from content.

    Returns a brief version with just the actionable items.
    """
    lines = content.split("\n")
    result = []
    current_heading = ""

    for line in lines:
        if line.startswith("# "):
            result.append(line)
        elif line.startswith("## "):
            current_heading = line
        elif line.strip().startswith("- [ ]") or line.strip().startswith("- [x]"):
            if current_heading:
                result.append("")
                result.append(current_heading)
                current_heading = ""
            result.append(line)

    return "\n".join(result)


def extract_standard(content: str) -> str:
    """Extract checklist items + key questions, excluding anti-patterns section.

    Returns a standard-detail version.
    """
    lines = content.split("\n")
    result = []
    in_antipatterns = False

    for line in lines:
        if re.match(r"^##\s+.*(?:Anti-Pattern|Smells to Flag|Vulnerabilities)", line, re.IGNORECASE):
            in_antipatterns = True
            continue
        if in_antipatterns and line.startswith("## "):
            in_antipatterns = False
        if not in_antipatterns:
            result.append(line)

    return "\n".join(result)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file.

    Returns (metadata_dict, body_content).
    """
    if not content.startswith("---"):
        return {}, content

    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}, content

    frontmatter_text = content[3 : 3 + end_match.start()]
    body = content[3 + end_match.end() :]

    # Simple YAML parsing (no external dependency needed)
    metadata = {}
    for line in frontmatter_text.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            # Handle lists
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
            metadata[key] = value

    return metadata, body


class BookLoader:
    """Loads and parses book research files and checklists."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.book_research_dir = project_root / "book_research"
        self.articles_dir = self.book_research_dir / "anthropic_articles"
        self.knowledge_dir = project_root / "knowledge"
        self.checklists_dir = self.knowledge_dir / "checklists"

    def get_book_file(self, book_id: str) -> Path | None:
        """Resolve a book ID to its file path."""
        if book_id.startswith("a"):
            # Article ID like "a01"
            num = book_id[1:]
            pattern = f"{num}_*.md"
            matches = list(self.articles_dir.glob(pattern))
        else:
            pattern = f"{book_id}_*.md"
            matches = list(self.book_research_dir.glob(pattern))

        return matches[0] if matches else None

    def read_book_section(self, book_id: str, section: str = "key_ideas") -> str:
        """Read a specific section from a book research file."""
        file_path = self.get_book_file(book_id)
        if not file_path or not file_path.exists():
            return f"Book '{book_id}' not found."

        content = file_path.read_text(encoding="utf-8")

        if section == "full":
            return content

        extracted = extract_section(content, section)
        if extracted:
            return extracted

        return f"Section '{section}' not found in book '{book_id}'."

    def read_checklist(
        self, task_type: str, detail_level: str = "standard"
    ) -> str:
        """Read a checklist file with the specified detail level."""
        checklist_path = self.checklists_dir / f"{task_type}.md"
        if not checklist_path.exists():
            return f"Checklist '{task_type}' not found."

        content = checklist_path.read_text(encoding="utf-8")

        if detail_level == "brief":
            return extract_items_only(content)
        elif detail_level == "standard":
            return extract_standard(content)
        else:  # detailed
            return content

    def filter_by_focus(self, content: str, focus: str) -> str:
        """Filter checklist content to sections matching the focus keyword."""
        if not focus:
            return content

        focus_terms = [f.strip().lower() for f in focus.split(",")]
        lines = content.split("\n")
        result = []
        include_section = False
        in_header = True

        for line in lines:
            # Always include the title
            if line.startswith("# ") and not line.startswith("## "):
                result.append(line)
                continue

            # Check if this is a section heading
            if line.startswith("## "):
                heading_lower = line.lower()
                include_section = any(term in heading_lower for term in focus_terms)
                if include_section:
                    result.append("")
                    result.append(line)
                in_header = False
                continue

            # Include frontmatter
            if in_header:
                result.append(line)
                if line.strip() == "---" and len(result) > 1:
                    in_header = False
                continue

            if include_section:
                result.append(line)

        # If no sections matched, return the full content with a note
        if len(result) <= 5:
            return f"No sections matching focus '{focus}' found. Returning full checklist.\n\n{content}"

        return "\n".join(result)

    def list_books(self) -> list[dict]:
        """List all available books."""
        books = []
        for f in sorted(self.book_research_dir.glob("[0-9][0-9]_*.md")):
            book_id = f.stem[:2]
            title = f.stem[3:].replace("_", " ").title()
            books.append({"id": book_id, "title": title, "file": str(f.relative_to(self.project_root))})
        return books

    def list_articles(self) -> list[dict]:
        """List all available Anthropic articles."""
        articles = []
        for f in sorted(self.articles_dir.glob("[0-9][0-9]_*.md")):
            article_id = f"a{f.stem[:2]}"
            title = f.stem[3:].replace("_", " ").title()
            articles.append({"id": article_id, "title": title, "file": str(f.relative_to(self.project_root))})
        return articles

    def list_checklists(self) -> list[dict]:
        """List all available task checklists."""
        checklists = []
        for f in sorted(self.checklists_dir.glob("*.md")):
            task_type = f.stem
            metadata, _ = parse_frontmatter(f.read_text(encoding="utf-8"))
            description = metadata.get("description", "")
            checklists.append({"task_type": task_type, "description": description})
        return checklists
