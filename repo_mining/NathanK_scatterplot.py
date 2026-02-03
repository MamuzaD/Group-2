import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os
from collections import Counter

scriptDirectory = os.path.dirname(os.path.abspath(__file__))
inputFile = os.path.join(scriptDirectory, "..", "data", "file_author_dates.csv")

def main():
    rawData = []

    # read CSV
    with open(inputFile, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row["date"], "%Y-%m-%d")
            rawData.append((row["file"], row["author"], date))

    # find the earliest commit date
    firstDate = min(d[2] for d in rawData)

    # convert to continuous week timeline
    data = []
    for file, author, date in rawData:
        week = (date - firstDate).days // 7
        data.append((file, author, week))

    # sort files by activity with the most touched files on the left
    file_counts = Counter(d[0] for d in data)
    files = [f for f, _ in file_counts.most_common()]

    authors = sorted(set(d[1] for d in data))

    # create a vector that stores file enumerations
    fileToX = {file: i+1 for i, file in enumerate(files)}
    authorToColor = {author: i for i, author in enumerate(authors)}

    x = []
    y = []
    colors = []

    # add file commit history data to vector, color code authors
    for file, author, week in data:
        x.append(fileToX[file])
        y.append(week)
        colors.append(authorToColor[author])
    
    # plot x and y coords
    plt.figure(figsize=(14, 8))
    plt.scatter(x, y, c=colors, cmap="tab20", alpha=0.7)

    plt.xticks(range(1, len(files)+1))
    plt.xlabel("File Number ")

    plt.ylabel("Time Passed (weeks)")
    plt.title("File Touches Author")

    # legend
    handles = []
    for author, idx in authorToColor.items():
        handles.append(
            plt.Line2D([0], [0], marker="o", color="w",
                       label=author,
                       markerfacecolor=plt.cm.tab20(idx / len(authors)),
                       markersize=8)
        )

    plt.legend(handles=handles, title="Authors",
               bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()