import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# ---
# CONFIG
# -----

input_csv = "author_file_touches.csv"
output_plot = "author_file_scatterplot.png"

# ---
# LOAD DATA 
# ----
records = []
with open(input_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        records.append({
            "file": row["file"],
            "author": row["author"],
            "date": datetime.strptime(row["date"], "%Y-%m-%d")
        })

# compute weeks from date and time 
# calc the start date from the earliest commit
start= min(r["date"] for r in records)
for r in records:
    r["week"] = (r["date"] - start).days // 7

# sort filenames and enumerate by author
files = sorted({r["file"] for r in records})
file_y_index = {file: idx for idx, file in enumerate(files)}
author_plotpoints = defaultdict(lambda: {"x": [], "y": []})
for r in records:
    author_plotpoints[r["author"]]["x"].append(r["week"])
    author_plotpoints[r["author"]]["y"].append(file_y_index[r["file"]])

# ---
# PLOT
# -----
plt.figure(figsize=(14,8))

for author, points in author_plotpoints.items():
    plt.scatter(
        points["x"], points["y"],
        s=25, alpha=0.75, label=author
    )

plt.yticks(range(len(files)))
plt.ylabel("File")
plt.xlabel("Weeks")
plt.title("Author Activity Over Time (scottyab/rootbeer)")
plt.savefig(output_plot, dpi=300)
plt.show()
print(f"Scatter plot saved as {output_plot}")
