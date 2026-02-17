import os
import csv
import requests
import time

# Defines repo thats grabbed from
REPO = "scottyab/rootbeer"

# creates directory for csv file to later be extracted in scatterplot
scriptDirectory = os.path.dirname(os.path.abspath(__file__))
dataDirectory = os.path.join(scriptDirectory, "..", "data")
os.makedirs(dataDirectory, exist_ok=True)

outputFile = os.path.join(dataDirectory, "file_author_dates.csv")

# github tokens (replace here)
tokens = [
    "replace tokens here"
]

# define source files
sourceExtensions = (
    ".java",
    ".kt",
    ".c",
    ".cpp",
    ".hpp",
)

includeFiles = {
    "CMakeLists.txt"
}

# request github
def githubRequest(url, tokenIndex):
    token = tokens[tokenIndex % len(tokens)]
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        r = requests.get(url, headers=headers)

        if r.status_code == 403 and "rate limit" in r.text.lower():
            print("Rate limit reached, sleeping 2 seconds...")
            time.sleep(2)
            continue

        r.raise_for_status()
        return r.json()

# determines if function is considered a source file
def isSourceFile(filename):
    lower = filename.lower()
    return lower.endswith(sourceExtensions) or filename in includeFiles

# grabs repo files
def getRepoFiles(repo):
    files = []
    stack = [""]
    tokenIndex = 0
    
    # opens path to repo, files act as a stack and pops extracted src files 
    while stack:
        path = stack.pop()
        url = f"https://api.github.com/repos/{repo}/contents/{path}"

        try:
            items = githubRequest(url, tokenIndex)
        except Exception as e:
            print(f"Error fetching contents at {path}: {e}")
            continue

        tokenIndex += 1

        for item in items:
            if item["type"] == "dir":
                stack.append(item["path"])

            elif item["type"] == "file":
                if isSourceFile(item["name"]):
                    files.append(item["path"])

    return files

# grabs commit history from a file
def getAllCommitsForFile(repo, filePath):
    allCommits = []
    page = 1
    tokenIndex = 0

    while True:
        url = (
            f"https://api.github.com/repos/{repo}/commits"
            f"?path={filePath}&per_page=100&page={page}"
        )

        try:
            commits = githubRequest(url, tokenIndex)
        except Exception as e:
            print(f"Error fetching commits for {filePath}: {e}")
            break

        if not commits:
            break

        for commit in commits:
            # prioritize github username
            if commit["author"]:
                author = commit["author"]["login"]
            else:
                author = commit["commit"]["author"]["name"]

            date = commit["commit"]["author"]["date"][:10]
            allCommits.append((filePath, author, date))

        page += 1
        tokenIndex += 1

    return allCommits


# main, calls functions
def main():
    print("Scanning repository for source files...")
    files = getRepoFiles(REPO)

    print(f"Found {len(files)} source files.")
    print("Collecting commit history...\n")

    allTouches = []

    for i, filePath in enumerate(files, start=1):
        print(f"[{i}/{len(files)}] Fetching commits: {filePath}")
        touches = getAllCommitsForFile(REPO, filePath)
        allTouches.extend(touches)
        print(f"  → {len(touches)} commits added")

    print(f"\nTotal commits collected: {len(allTouches)}")

    # write to csv
    with open(outputFile, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file", "author", "date"])
        writer.writerows(allTouches)

    print(f"\nSaved CSV to: {outputFile}")


if __name__ == "__main__":
    main()
