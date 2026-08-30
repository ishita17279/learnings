import json
import os

from github import Github


GITHUB_TOKEN = os.getenv["GITHUB_TOKEN"]
REPOSITORY = "ishita17279/learnings"


github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPOSITORY)


learnings = []


for pr in repo.get_pulls(state="closed"):

    # Only merged PRs
    if not pr.merged:
        continue

    body = pr.body or ""

    # Ignore PRs without #donts
    if "#donts" not in body.lower():
        continue

    learning = {
        "pr_number": pr.number,
        "title": pr.title,
        "author": pr.user.login,
        "url": pr.html_url,
        "content": body,
    }

    learnings.append(learning)


with open("data/learnings.json", "w") as file:
    json.dump(
        {"learnings": learnings},
        file,
        indent=2,
    )


print(f"Collected {len(learnings)} learnings.")