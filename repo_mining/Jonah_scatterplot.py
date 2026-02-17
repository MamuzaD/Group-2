import csv
from datetime import datetime

import plt

def mapToNum(lst):
    i = 0
    dict = {}
    for _, item in enumerate(lst):
        if item not in dict:
            dict[item] = i
            i += 1

    newList = []
    for item in lst:
        newList.append(dict[item])

    return newList, dict

def get_earliest_date(fileName):
    in_file = open(fileName, 'r')
    rdr = csv.reader(in_file)
    next(rdr)
    earliest_date = None
    for row in rdr:
        date = row[2]
        if earliest_date is None or date < earliest_date:
            earliest_date = date

    in_file.close()
    return datetime.fromisoformat(earliest_date)

repo = 'scottyab/rootbeer'
file = repo.split('/')[1]
fileInput = 'data/authors_' + file + '.csv'


start_time = get_earliest_date(fileInput)
inputCSV = open(fileInput, 'r')
reader = csv.reader(inputCSV)

filenames = []
authors = []
weeks = []

next(reader)
for row in reader:
    filename = row[0]
    author = row[1]
    date = row[2]
    week = (datetime.fromisoformat(date) - start_time).days / 7.0

    filenames.append(filename)
    authors.append(author)
    weeks.append(week)


filenameList, _ = mapToNum(filenames)
authorList, _ = mapToNum(authors)

plt.scatter(filenameList, weeks, c=authorList)

plt.xlabel('File')
plt.ylabel('Weeks')
plt.title('Scatterplot of Weeks vs File')


plt.show()

inputCSV.close()

