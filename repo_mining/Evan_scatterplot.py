import matplotlib.pyplot as plt
import pandas as pd

history = pd.read_csv("data/file_history.csv")

history["commit_date"] = pd.to_datetime(history["commit_date"], utc=True)

start = history["commit_date"].min()
history["weeks"] = ((history["commit_date"] - start).dt.days // 7)

history = history.sort_values("weeks")


history["author_id"], _ = pd.factorize(history["author_email"])
history["file_id"], _ = pd.factorize(history["filename"])


plt.scatter(history["file_id"], history["weeks"], c=history["author_id"])

plt.xlabel("file")
plt.ylabel("weeks")

plt.savefig("history_scatterplot.png")