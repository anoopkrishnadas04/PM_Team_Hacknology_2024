import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import get_anime_list
anime_df = pd.read_csv('anime-dataset-2023.csv')

# Split genres and create a list of all genres excluding the specified ones
anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]

all_genres = anime_df['Genres'].str.split(', ').explode()

tv_anime_df = anime_df[anime_df['Type'] == 'TV'] #Include only TV data as to not skew results

# Assuming anime_df is your DataFrame with a column named 'Genres'

# Create a list of unique genres
genres_tv = tv_anime_df['Genres'].str.split(', ').explode().unique()

  # Create a binary matrix where each row represents an anime and each column represents a genre
binary_matrix_tv = pd.DataFrame(columns=genres_tv)


for genre in genres_tv:
    binary_matrix_tv[genre] = tv_anime_df['Genres'].apply(lambda x: 1 if genre in x else 0)
    
# Create a heatmap
corr_matrix_tv = binary_matrix_tv.corr()


user_genres = get_anime_list.get_anime_list_genres(get_anime_list.get_anime_list("TheYellowInvader"))
sum = 0
for key in list(user_genres.keys()):
    sum += user_genres[key]
def add_genre_score(genres): 
    #assuming i have a list of the genres that I need to check
    count = 0
    target_anime_genres = genres.split(', ')
    for x in user_genres.keys():
        for y in target_anime_genres:
            #you can add the weight values in at this point by just multipling the value of corr_matrix_tv by the weight
            count += (corr_matrix_tv[x][y]*user_genres[x]/sum)
    return str(1 + count)

tv_anime_df['genre likeness'] = tv_anime_df['Genres'].apply(add_genre_score)
print(tv_anime_df.sort_values(by='genre likeness', ascending=False).head())


#print(corr_matrix_tv)
# print(corr_matrix_tv['Action']['Comedy'])