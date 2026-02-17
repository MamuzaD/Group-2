import os
import csv
import requests
from pathlib import Path

# Added token authentication to get past rate limiting
# Token was set in terminal env with
# $env:GITHUB_TOKEN="<token>"
HEADERS = {"Accept": "application/vnd.github+json"}
token = os.environ.get("GITHUB_TOKEN")
if token:
    HEADERS["Authorization"] = f"token {token}"

script_dir = Path(__file__).resolve().parent
data_path = script_dir / "data"

input_csv = data_path / "file_rootbeer.csv"
output_csv = data_path / "authorsFileTouches_rootbeer.csv"

tracked_files = set()

with open(input_csv, newline='', encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        if not row:
            continue

        if row[0].strip().lower() == "filename":
            continue

        tracked_files.add(row[0].strip())

with open(output_csv, "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out)
    writer.writerow(["filename", "author", "date"])
    print("Collecting commits from tracked files...")

    page = 1
    while True:
        # Hardcoding the url for commits since we're doing rootbeer
        commits_url = f"https://api.github.com/repos/scottyab/rootbeer/commits"
        commits = requests.get(commits_url,
                               params={"per_page": 100,
                                       "page": page},
                               headers=HEADERS).json()
        if not isinstance(commits, list):
            print("Unexpected response type: ", commits.get("message", commits))
            break

        if not commits:
            break

        for commit in commits:
            sha = commit["sha"]
            commit_url = f"https://api.github.com/repos/scottyab/rootbeer/commits/{sha}"
            details = requests.get(commit_url, headers=HEADERS).json()

            if "commit" not in details:
                print("Unexpected message:", details.get("message", "unknown error"))
                continue

            author = details["commit"]["author"]["name"]
            date = details["commit"]["author"]["date"]

            for f in details.get("files", []):
                filename = f["filename"]
                if filename in tracked_files:
                    writer.writerow([filename, author, date])

            # print(f"Commit: {author}, {date}")
        page += 1

print("Completed. Output written to: ", output_csv)
