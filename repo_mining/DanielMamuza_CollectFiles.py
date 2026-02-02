import json
import requests
import csv

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


def is_src_file(filename: str) -> bool:
    # must be under app/ or rootbeerlib/ directory
    if not (filename.startswith("app/") or filename.startswith("rootbeerlib/")):
        return False

    # exclude test files
    if "/test/" in filename.lower() or "/androidtest/" in filename.lower():
        return False

    if filename.endswith("CMakeLists.txt"):
        return True

    # whitelist of source code extensions
    source_extensions = {".java", ".kt", ".cpp", ".c", ".h", ".cmake"}
    _, ext = os.path.splitext(filename.lower())

    return ext in source_extensions


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictAllFiles, dictSrcFiles, lsttokens, repo):
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
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = "https://api.github.com/repos/" + repo + "/commits/" + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails["files"]
                for filenameObj in filesjson:
                    filename = filenameObj["filename"]
                    dictAllFiles[filename] = dictAllFiles.get(filename, 0) + 1

                    if is_src_file(filename):
                        dictSrcFiles[filename] = dictSrcFiles.get(filename, 0) + 1
                        print(f"[SOURCE] {filename}")
                    else:
                        print(f"[OTHER]  {filename}")
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)


# GitHub repo
repo = "scottyab/rootbeer"
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# NOTE :: preferring to use environment vars instead - daniel

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
# lstTokens = [
#     "fd02a694b606c4120b8ca7bbe7ce29229376ee",
#     "16ce529bdb32263fb90a392d38b5f53c7ecb6b",
#     "8cea5715051869e98044f38b60fe897b350d4a",
# ]


def write_csv(filename, dictfiles):
    rows = ["Filename", "Touches"]

    fileCSV = open(filename, "w")
    writer = csv.writer(fileCSV)
    writer.writerow(rows)

    bigcount = None
    bigfilename = None
    for filename, count in dictfiles.items():
        rows = [filename, count]
        writer.writerow(rows)
        if bigcount is None or count > bigcount:
            bigcount = count
            bigfilename = filename
    fileCSV.close()

    if bigfilename is not None:  # fix pyright type issue - daniel
        print(
            "The file " + bigfilename + " has been touched " + str(bigcount) + " times."
        )
    return bigfilename, bigcount


def main():
    lstTokens = load_tokens()
    dictAllFiles = dict()
    dictSrcFiles = dict()
    countfiles(dictAllFiles, dictSrcFiles, lstTokens, repo)
    print("Total number of files: " + str(len(dictAllFiles)))

    file = repo.split("/")[1]
    # write general CSV (all files)
    fileOutputAll = "data/file_" + file + ".csv"
    write_csv(fileOutputAll, dictAllFiles)

    # write source files CSV
    fileOutputSrc = "data/file_" + file + "_src.csv"
    write_csv(fileOutputSrc, dictSrcFiles)


if __name__ == "__main__":
    main()
