import csv
import json
import requests

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


def is_source_file(filename):
    #return true if file is in app/src directory
    return filename.startswith('app/src')
def get_commits(filename, lsttokens, repo, ct):
    try:

        url = 'https://api.github.com/repos/' + repo + '/commits?path=' + filename
        jsonCommits, ct = github_auth(url, lsttokens, ct)
        res = []
        for jsonCommit in jsonCommits:
            commit = jsonCommit['commit']
            author_data = commit['author']
            author = author_data['name']
            date = author_data['date']

            res.append([author, date])

        return res, ct

        #parse into array of author and timestamp


    except Exception as e:
        print(e)


    return [], ct

lstTokens = []

repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
fileInput = 'data/file_' + file + '.csv'
fileOutput = 'data/authors_' + file + '.csv'

inputCSV = open(fileInput, 'r')
outputCSV = open(fileOutput, 'w')


reader = csv.reader(inputCSV)
writer = csv.writer(outputCSV)

writer.writerow(['Filename', 'Author','Date'])
ct = 0
for row in reader:
    filename = row[0]
    numTouches = row[1]

    #get timestamp of all commits for filename.
    if is_source_file(filename):
        commits, ct = get_commits(filename, lstTokens, repo, ct)

        for commit in commits:
            author = commit[0]
            date = commit[1]
            writer.writerow([filename, author, date])
            print(filename, author, date, 'commit found')

inputCSV.close()
outputCSV.close()
