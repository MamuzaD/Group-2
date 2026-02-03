import pandas as pd
import json
import requests

df = pd.read_csv("data/file_rootbeer.csv")

# GitHub repo
repo = 'scottyab/rootbeer'
# tokens
lsttokens = ["nuh uh"]

def getHistory(lsttokens, repo):
    def __github_auth(url, lsttoken, ct):
        jsonData = None
        try:
            ct = ct % len(lsttokens)
            headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
            request = requests.get(url, headers=headers)
            jsonData = json.loads(request.content)
            ct += 1
        except Exception as e:
            pass
            print(e)
        return jsonData, ct

    ipage = 1  # url page counter
    ct = 0  # token counter

    result = []

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = __github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                author_email = shaObject["commit"]["author"]["email"]
                commit_date = shaObject["commit"]["author"]["date"]

                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = __github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    if filename not in df["Filename"].values:
                        continue

                    # Check for code files
                    if not any([filename.endswith(x) for x in [".java", ".kt", ".cpp", ".h", "CMakeLists.txt"]]):
                        continue
                    # check for C/C++/CMake code files in correct location
                    elif any([filename.endswith(x) for x in [".cpp", ".h", "CMakeLists.txt"]]) and "rootbeerlib/src/main/cpp/" not in filename:
                        continue
                    # check for kotlin files in correct location
                    elif filename.endswith(".kt") and "app/src/main/java" not in filename:
                        continue
                    # check for java files in correct location
                    elif filename.endswith(".java") and "rootbeerlib/src/main/java" not in filename:
                        continue

                    result.append({
                        "author_email": author_email,
                        "commit_date": commit_date,
                        "filename": filename,
                    })

            ipage += 1
    except:

        print("Error receiving data")
        exit(0)

    return pd.DataFrame(result)


result_df = getHistory(lsttokens, repo)

result_df.to_csv("data/file_history.csv", index=False)