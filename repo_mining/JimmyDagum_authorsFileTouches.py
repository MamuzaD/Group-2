from dotenv import load_dotenv
import os
import csv
import time
import requests

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not found. Put it in .env and re-run.")

REPO = "scottyab/rootbeer"
IN_CSV = os.path.join("data", "source_file_rootbeer.csv")
OUT_CSV = os.path.join("data", "rootbeer_file_touches_by_author.csv")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def gh_get(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params, timeout=60)

    # Basic rate limit handling
    if r.status_code == 403 and "rate limit" in r.text.lower():
        print("Rate limited. Sleeping 15s and retrying...")
        time.sleep(15)
        return gh_get(url, params)

    if r.status_code != 200:
        print("GitHub API error", r.status_code, "for", url)
        print(r.text[:500])
        return None

    return r.json()

def iter_commits_for_file(path):
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPO}/commits"
        data = gh_get(url, params={"path": path, "per_page": 100, "page": page})
        if not data:
            break

        for item in data:
            commit = item.get("commit", {})
            ca = commit.get("author") or {}
            date_iso = ca.get("date")

            # Prefer GitHub login if available; else fallback to commit author name
            author_login = (item.get("author") or {}).get("login")
            author_name = ca.get("name") or "UNKNOWN"
            author = author_login or author_name

            if date_iso:
                yield author, date_iso

        page += 1

def main():
    # Read file list from adapted CollectFiles output
    files = []
    with open(IN_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            files.append(row["Filename"])

    print(f"Loaded {len(files)} source files from {IN_CSV}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "author", "date_iso"])

        for i, path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] {path}")
            seen = set()  # avoid duplicate author+date rows if API repeats
            for author, date_iso in iter_commits_for_file(path):
                key = (author, date_iso)
                if key in seen:
                    continue
                seen.add(key)
                w.writerow([path, author, date_iso])

    print("Wrote:", OUT_CSV)

if __name__ == "__main__":
    main()
