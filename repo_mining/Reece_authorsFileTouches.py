import json
import requests
import csv
import os
if not os.path.exists("data"):
    os.makedirs("data")

class Commit:
    def __init__(self, number, date, name, login, touched_files):
        self.number = number  
        self.date = date  
        self.name = name
        self.login = login
        self.touched_files = touched_files

    def details(self):
        print(f"\nCommit: {self.number}")
        print(f"Date: {self.date}")
        print(f"Author Name: {self.name}")
        print(f"Author Login: {self.login}")
        print(f"Touched Source Files: {self.touched_files}")

class SourceFile:
    def __init__(self, date, name, login):
        self.date = date  
        self.name = name
        self.login = login

# All source files begin with the paths below.
javasrc = "rootbeerlib/src/main/java"
cppsrc = "rootbeerlib/src/main/cpp"
ktsrc = "app/src/main/java/com/scottyab/rootbeer/sample/"
srcfiles = [javasrc, cppsrc, ktsrc]

# List of Commit objects.
allCommits = []

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    itr = 0

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'

            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                itr = itr + 1
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
        
                try:
                    name = shaDetails['commit']['author']['name']
                except:
                    name = ""
                try:
                    login = shaDetails['author']['login']
                except:
                    login = ""
                try:
                    date = shaDetails['commit']['author']['date']
                except:
                    date = ""

                touched_files = []

                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    for srcfile in srcfiles:
                        if filename.startswith(srcfile):
                            touched_files.append(filename)
                            dictfiles[filename] = dictfiles.get(filename, 0) + 1
                            break
                
                print(touched_files)
                commit = Commit(itr, date, name, login, touched_files)
                allCommits.append(commit)
                commit.details()
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

touch_history = []
for commit in allCommits:
    for srcfile in commit.touched_files:
        touch_history.append([srcfile, commit.date, commit.name, commit.login])

with open('data/Reece_authorFileTouches.csv', 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["file", "date", "name", "login"])
    writer.writerows(touch_history)

