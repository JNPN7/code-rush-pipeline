import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import seaborn as sns
import json
import ast

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

with open("./data/natalie_portman.json", 'r') as f:
    data = json.load(f)
    data = ast.literal_eval(data)

celeb_name = data["name"]
celeb_profession = data["profession"]

df = pd.DataFrame(data["works"])

# Extract start-year
year = df["year"].str.split("\\u2013", n = 1, expand = True)
df["start-year"] = year[0]
df["start-year"] = df["start-year"].astype(int)
#df["end-year"] = year[1]

# Plot bar graph of genre
plt.title("Genre bar plot")
genres = list(df['genre'])
genre = []
for gen in genres:
    genre.extend(gen)

genre = pd.DataFrame(genre)
genre[0].value_counts().plot(kind='bar');
plt.show()


# Plot bar graph of year
plt.title("Year vs Count plot")
df_sorted = df.sort_values("start-year")
df_sorted["start-year"].value_counts(sort=False).plot(kind='bar')
plt.show()

# Plot rating graph
df.reset_index().plot.scatter(x="index", y="rating", title="Rating plot")
plt.show()

df.plot.scatter(x="start-year", y="rating", title="Year vs Rating plot")
plt.show()
