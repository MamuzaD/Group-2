import json
import requests
import csv
from typing import Set

import os

if not os.path.exists("data"):
    os.makedirs("data")


def load_tokens() -> list[str]:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass

    tokens_csv = os.getenv("GITHUB_TOKENS", "").strip()
    if tokens_csv:
        return [t.strip() for t in tokens_csv.split(",") if t.strip()]

    token = os.getenv("GITHUB_TOKEN", "").strip()
    return [token] if token else []


# GitHub Authentication function
def github_auth(url, tokens, ct):
    jsonData = None
    try:
        ct = ct % len(tokens)
        headers = {"Authorization": "Bearer {}".format(tokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
        raise e
    return jsonData, ct


def load_source_files(csv_path) -> Set[str]:
    source_files = set()
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_files.add(row["Filename"])
    return source_files


def collect_authors(
    src_files,
    lsttokens,
    repo,
):
    files = []
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = (
                "https://api.github.com/repos/"
                + repo
                + "/commits?page="
                + spage
                + "&per_page=100"
            )
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject["sha"]
                commit = shaObject["commit"]
                msg = commit["message"]
                author = commit["author"]["name"]
                date = commit["author"]["date"]

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails["files"]
                i = 0
                for filenameObj in filesjson:
                    filename = filenameObj["filename"]

                    if filename in src_files:
                        files.append((filename, author, date))
                        i += 1

                if i > 0:
                    first_line = msg.split("\n", 1)[0]
                    print(f"Found {i} files in {first_line}")

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return files


# GitHub repo
repo = "scottyab/rootbeer"


def main():
    lstTokens = load_tokens()
    if not lstTokens or lstTokens[0] == "":
        print("ERROR: No GitHub token found.")
        exit(1)

    file = repo.split("/")[1]

    src_filename = "data/file_" + file + "_src.csv"
    src_files = load_source_files(src_filename)
    files = collect_authors(
        src_files,
        lstTokens,
        repo,
    )
    print("Total number of touches on source files: " + str(len(files)))

    # write authors and dates CSV
    fileOutput = "data/file_" + file + "_authors.csv"
    rows = ["Filename", "Author", "Date"]
    fileCSV = open(fileOutput, "w")
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    for filename, author, date in files:
        rows = [filename, author, date]
        writer.writerow(rows)
    fileCSV.close()


if __name__ == "__main__":
    main()
