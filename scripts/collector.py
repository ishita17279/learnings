import json
import os

from github import Github


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPOSITORY = "ishita17279/learnings"


github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPOSITORY)


def extract_subsections(text):
    """
    Extract all ## subsections from the # Donts section.
    """

    lines = text.splitlines()

    sections = {}
    current_heading = None
    current_content = []

    for line in lines:

        stripped_line = line.strip()

        # New ## subsection
        if stripped_line.startswith("## "):

            # Save previous subsection
            if current_heading:
                sections[current_heading] = "\n".join(
                    current_content
                ).strip()

            current_heading = (
                stripped_line[3:]
                .strip()
                .lower()
                .replace(" ", "_")
            )

            current_content = []

        # Content of current subsection
        elif current_heading:
            current_content.append(stripped_line)

    # Save final subsection
    if current_heading:
        sections[current_heading] = "\n".join(
            current_content
        ).strip()

    return sections


learnings = []


for pr in repo.get_pulls(state="closed"):

    # Only process merged PRs
    if not pr.merged:
        continue

    body = pr.body or ""
    lines = body.splitlines()

    # Find # Donts section
    donts_start = None

    for index, line in enumerate(lines):

        if line.strip().lower() == "# donts":
            donts_start = index
            break

    # No # Donts section
    if donts_start is None:
        continue

    # Find the end of # Donts section
    donts_end = len(lines)

    for index in range(donts_start + 1, len(lines)):

        if lines[index].strip().startswith("# "):
            donts_end = index
            break

    # Extract only content inside # Donts
    donts_section = "\n".join(
        lines[donts_start + 1:donts_end]
    ).strip()

    # Extract all ## subsections dynamically
    content = extract_subsections(donts_section)

    learning = {
        "pr_number": pr.number,
        "title": pr.title,
        "author": pr.user.login,
        "url": pr.html_url,
        "content": content,
    }

    learnings.append(learning)


with open("data/learnings.json", "w") as file:

    json.dump(
        {"learnings": learnings},
        file,
        indent=2,
    )


print(f"Collected {len(learnings)} learnings.")