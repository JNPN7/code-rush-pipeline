import scraper
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import seaborn as sns

a = scraper.Scraper()

data = a.get_top250_movies_info()

# Load data into a dataframe
df = pd.DataFrame.from_dict(data)

# Replace non-numeric values in the year and rating columns with NaN
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Drop any rows with NaN values
df = df.dropna()

# Convert year to integer type
df['year'] = df['year'].astype(int)

# Extract the first genre for each movie
df['genre'] = df['genre'].apply(lambda x: x[0])

# Plot a box plot of the ratings for each genre
sns.boxplot(x='genre', y='rating', data=df)
plt.xlabel('Genre')
plt.ylabel('Rating')
plt.title('Movie Genre Popularity by Rating')
plt.show()

# Concatenate all the genres into a single string
all_genres = " ".join(df['genre'].tolist())

# Plot a wordcloud of the genres
wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=None, min_font_size=10).generate(all_genres)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()

# Group the data by year
grouped = df.groupby('year')

# Create a list to store the data for each year
years = []
titles = []
ratings = []

# Loop over each group and extract the data
for year, group in grouped:
    max_rating = group['rating'].max()
    movie = group[group['rating'] == max_rating].iloc[0]
    years.append(year)
    titles.append(movie['titles'])
    ratings.append(max_rating)

# Create a dataframe with the extracted data
data = {'year': years, 'titles': titles, 'rating': ratings}
high_rating_movies = pd.DataFrame(data)

# Plot the data
plt.plot(high_rating_movies['year'], high_rating_movies['rating'], color='red')

# Add the movie title to the x axis labels
plt.xticks(high_rating_movies['year'], ["{} ({})".format(title, year) for title, year in zip(high_rating_movies['titles'], high_rating_movies['year'])], rotation=90)

# Add axis labels and a title
plt.xlabel('Year and Movie Title')
plt.ylabel('Rating')
plt.title('Movie with highest rating for each year')

# Show the plot
plt.show()
