import csv
from datetime import datetime
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import requests
import re

script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

input_csv = data_dir / "authorsFileTouches_rootbeer.csv"

rows = []

with open(input_csv, newline='') as file:
    reader = csv.reader(file)
    next(reader)    # header skip
    for row in reader:
        filename, author, date_str = row
        date = datetime.fromisoformat(date_str.replace("Z", ""))
        rows.append([filename, author, date])

# Assign each file a number and sort files by date of first touch
first_touch = {}
for filename, _, date in rows:
    if filename not in first_touch or date < first_touch[filename]:
        first_touch[filename] = date

sorted_files = sorted(first_touch, key=lambda x: first_touch[x])
file_ids = {filename: i for i, filename in enumerate(sorted_files)}

# Get inital repo commit so we can start from project start if it's not in the src
url = "https://api.github.com/repos/scottyab/rootbeer/commits"

resp = requests.get(url, params={"per_page": 1})
last_page_url = resp.links["last"]["url"]

oldest_commit = requests.get(last_page_url).json()[0]
start_date_str = oldest_commit["commit"]["author"]["date"]
start_date = datetime.fromisoformat(start_date_str.replace("Z", ""))

x = []
y = []
colors = []

# Create author ids to get different colors from each one instead of
# hashing in the plot to get consistent colors per author
author_ids = {}
next_author_id = 0

for _, author, _ in rows:
    if author not in author_ids:
        author_ids[author] = next_author_id
        next_author_id += 1

for filename, author, date in rows:
    file_id = file_ids[filename]
    week = (date - start_date).days // 7

    x.append(file_id)
    y.append(week)
    colors.append(author_ids[author])

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colors)

plt.xlabel("file")
plt.ylabel("weeks")

plt.show()
