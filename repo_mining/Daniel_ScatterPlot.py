import csv
from collections import Counter
from datetime import date, datetime as dt

import matplotlib as mpl
import matplotlib.pyplot as plt


# GitHub repo
repo = "scottyab/rootbeer"


def load_authors_data(csv_path: str) -> list[tuple]:
    data = []
    fileCSV = open(csv_path, "r")
    reader = csv.DictReader(fileCSV)
    for row in reader:
        data.append((row["Filename"], row["Author"], row["Date"]))
    fileCSV.close()
    return data


def load_src_files(csv_path: str) -> list[tuple]:
    files = []
    fileCSV = open(csv_path, "r")
    reader = csv.DictReader(fileCSV)
    for row in reader:
        files.append(row["Filename"])
    fileCSV.close()
    return files


def weeks_since_start(date: date, start_date: date) -> int:
    delta = date - start_date
    return int(delta.days / 7)


def assign_author_colors(sorted_authors: list) -> dict:
    n = len(sorted_authors)

    cmap10 = mpl.colormaps["tab10"]
    cmap20 = mpl.colormaps["tab20"]
    colors = [cmap10(i) for i in range(10)]  # best colors for top 10
    colors.extend([cmap20(i) for i in range(n - 10)])

    mapping = {author: colors[i] for i, author in enumerate(sorted_authors)}
    return mapping


def main():
    file = repo.split("/")[1]
    authors_csv = "data/file_" + file + "_authors.csv"
    src_csv = "data/file_" + file + "_src.csv"

    data = load_authors_data(authors_csv)
    src_files = load_src_files(src_csv)

    dates = [dt.fromisoformat(d) for _, _, d in data]
    start_date = min(dates)
    file_to_id = {f: i for i, f in enumerate(src_files)}  # get dates order from src.csv

    authors = [a for _, a, _ in data]
    author_counts = Counter(authors)
    # sort by most active first, then alphabetically
    sorted_authors = sorted(set(authors), key=lambda a: (-author_counts[a], a))
    author_to_color = assign_author_colors(sorted_authors)

    print(
        f"Info Totals:\n\tTouches: {len(data)}\n\tSrc files: {len(src_files)}\n\tAuthors: {len(author_to_color)}"
    )

    # prepare data for plot
    file_ids = []
    weeks_list = []
    colors = []
    for i, (filename, author, _) in enumerate(data):
        file_ids.append(file_to_id[filename])
        weeks_list.append(weeks_since_start(dates[i], start_date))
        colors.append(author_to_color[author])

    # scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(
        file_ids,
        weeks_list,
        c=colors,
        s=50,
        alpha=0.7,
        edgecolors="black",
        linewidth=0.4,
    )
    plt.title(f"{repo} - src file touches")

    # axes
    plt.ylabel("weeks")
    plt.xlabel("file")
    plt.xticks(range(0, len(src_files), 2))

    # legend
    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=author_to_color[a],
            markersize=10,
            label=f"{a} ({author_counts[a]})",
        )
        for a in sorted_authors
    ]
    plt.legend(
        handles=handles,
        title="Authors (sorted by most touches)",
        bbox_to_anchor=(1, 1.015),
        loc="upper left",
    )
    plt.tight_layout()

    # save image
    output_file = "data/file_" + file + "_scatterplot.png"
    plt.savefig(output_file)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass  # ignore KeyboardInterrupt


if __name__ == "__main__":
    main()
