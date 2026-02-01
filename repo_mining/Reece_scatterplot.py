import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone

# Translate Pandas df column from dates to weeks since first touch.
def convertWeeksLifetime(date_column):
    date_column = pd.to_datetime(date_column)
    first_touch = date_column.min()
    days_since = date_column - first_touch
    weeks_since = days_since.dt.days / 7  
    return weeks_since

# To create a scatter plot, it must take in the CSV file created by "Reece_authorsFileTouches.py"
df = pd.read_csv("data/authorFileTouches.csv")

# Reverse the dataframe.
df = df.iloc[::-1]

# Encode file names with numbers.
df.insert(1, "encoded", df["file"].factorize()[0])
x = df['encoded']

# Turn dates into weeks since.
df['date'] = convertWeeksLifetime(df['date'])
df.rename(columns = {"date": "weeks"}, inplace = True)
y = df['weeks']

# Print dataframe to console.
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df)

# Display Pyplot dot chart.
plt.figure()

# Each colored dot represents a different author.
for name in df["name"].unique():
    subset = df[df["name"] == name]
    plt.scatter(subset["encoded"], subset["weeks"], alpha = 0.7, label = name, s = 20)
    
plt.xticks(df["encoded"])
plt.xlabel("File") # Every unique file is encoded with a number.
plt.ylabel("Weeks") # Number of weeks since start of project file was touched.

plt.legend(title = "Authors", loc = "upper left", bbox_to_anchor = (1, 1), fontsize = "small", markerscale = 1.25)
plt.tight_layout()
plt.show()
