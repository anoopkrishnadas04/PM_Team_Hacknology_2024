import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def get_heatmap_table():
    anime_df = pd.read_csv('anime-dataset-2023.csv')

    # Split genres and create a list of all genres excluding the specified ones
    anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]

    all_genres = anime_df['Genres'].str.split(', ').explode()

    tv_anime_df = anime_df[anime_df['Type'] == 'TV'] #Include only TV data as to not skew results

    # Assuming anime_df is your DataFrame with a column named 'Genres'

    # Create a list of unique genres
    genres_tv = tv_anime_df['Genres'].str.split(', ').explode().unique()

    print(genres_tv)

    # Create a binary matrix where each row represents an anime and each column represents a genre
    binary_matrix_tv = pd.DataFrame(columns=genres_tv)


    for genre in genres_tv:
        binary_matrix_tv[genre] = tv_anime_df['Genres'].apply(lambda x: 1 if genre in x else 0)
    
    # Create a heatmap
    corr_matrix_tv = binary_matrix_tv.corr()

    print(corr_matrix_tv)
    # print(corr_matrix_tv['Action']['Comedy'])

    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix_tv, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation Heatmap of Genres')
    plt.show()

    return genres_tv

get_heatmap_table()