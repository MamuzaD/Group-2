import os
import csv
from datetime import datetime, timezone
from collections import defaultdict

import matplotlib.pyplot as plt

IN_CSV = os.path.join("data", "rootbeer_file_touches_by_author.csv")
OUT_PNG = os.path.join("data", "rootbeer_scatter.png")

def parse_iso(s: str) -> datetime:
    # Handles trailing Z
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)

def main():
    rows = []
    files_set = set()
    authors_set = set()
    dates = []

    with open(IN_CSV, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            file = row["file"]
            author = row["author"]
            dt = parse_iso(row["date_iso"])

            rows.append((file, author, dt))
            files_set.add(file)
            authors_set.add(author)
            dates.append(dt)

    if not rows:
        raise RuntimeError("No rows found. Did script 1 generate the CSV correctly?")

    # Week 0 is the earliest week in project lifetime
    start = min(dates)

    def week_index(dt: datetime) -> int:
        delta_days = (dt - start).days
        return delta_days // 7

    files = sorted(files_set)
    authors = sorted(authors_set)

    file_to_y = {f: i for i, f in enumerate(files)}
    author_to_i = {a: i for i, a in enumerate(authors)}

    xs, ys, cs = [], [], []
    for file, author, dt in rows:
        xs.append(week_index(dt))
        ys.append(file_to_y[file])
        cs.append(author_to_i[author])

    plt.figure(figsize=(14, max(6, len(files) * 0.08)))
    plt.scatter(xs, ys, c=cs, s=14, alpha=0.75)

    plt.xlabel("Weeks since project start (week 0 = earliest touch)")
    plt.ylabel("File")
    plt.yticks(range(len(files)), files, fontsize=6)
    plt.title("scottyab/rootbeer — File touches over time (colored by author)")

    # Legend: If there are many authors, legend becomes unreadable.
    # Show top N authors by number of touches.
    counts = defaultdict(int)
    for _, author, _ in rows:
        counts[author] += 1
    top_authors = sorted(authors, key=lambda a: counts[a], reverse=True)[:12]

    handles = []
    labels = []
    for a in top_authors:
        # dummy handle for legend (color mapping is implicit)
        handles.append(plt.Line2D([0], [0], marker='o', linestyle='', markersize=6))
        labels.append(f"{a} ({counts[a]})")

    plt.legend(handles, labels, title="Top authors (touch count)", loc="upper right")
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200)
    print("Saved:", OUT_PNG)

if __name__ == "__main__":
    main()
