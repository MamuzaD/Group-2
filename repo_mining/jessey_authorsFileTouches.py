import requests
import csv

# ----------
# CONFIG
# --------

git_token = "FAKE_TOKEN"
owner = "scottyab"
repo = "rootbeer"

headers = {'Authorization': f"Bearer {git_token}", }
# -----
# HELPERS
# ------
def get_commits(file_path):
    # track files, author, and dates
    commit_results = []
    page = 1

    # newest 100 commits per loop
    while True:
        url = (
            f"https://api.github.com/repos/{owner}/{repo}/commits"
            f"?path={file_path}&per_page=100&page={page}"
        )

        request_result = requests.get(url, headers = headers)
        # 200, request accepted
        if request_result.status_code != 200:
            break

        
        commits = request_result.json()
        # empty list, paging is finished
        if not commits:
            break

        for commit in commits:
            # check for available GitHub username or use metadata name
            if commit["author"]:
                author = commit["author"]["login"]
            else:
                author = commit["commit"]["author"]["name"]

            # Extract date 
            date = commit["commit"]["author"]["date"][:10]

            commit_results.append((file_path, author, date))

        page += 1

    return commit_results

# ------
# MAIN
# ------

def main():
    input_csv = "data/file_rootbeer.csv"
    output_csv = "author_file_touches.csv"

    # track files visited
    files = []

    # read filenames from file_rootbeer.csv
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            files.append(row["Filename"])

    print(f"Total source files: {len(files)}\n")

    # fetch commits
    total_touches = []
    for i, file_path in enumerate(files, start=1):
        print(f"[{i}/{len(files)}] Fetching commits for {file_path}")
        touches = get_commits(file_path)
        total_touches.extend(touches)
        print(f"Total commits found: {len(touches)} \n")

    # write results to output csv
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "author", "date"])
        writer.writerows(total_touches)

    print(f"Output written to {output_csv}")

if __name__ == "__main__":
    main()

    



