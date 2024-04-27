import pandas as pd
import get_anime_list as gal
def compute_genre_likeness(anime_df, id_arr, user_anime_id):
    # Split genres and create a list of all genres excluding the specified ones
    anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]


    # split the genres of the users favorite anime and then add them to the waiting

    favorite_anime_genres = anime_df[anime_df['anime_id'] == user_anime_id]['Genres'].values[0].split(',')


    # Create a list of unique genres
    genres_tv = anime_df['Genres'].str.split(', ').explode().unique()

    # Create a binary matrix where each row represents an anime and each column represents a genre
    binary_matrix = pd.DataFrame(columns=genres_tv)


    for genre in genres_tv:
        binary_matrix[genre] = anime_df['Genres'].apply(lambda x: 1 if genre in x else 0)
        
    # Create a heatmap
    corr_matrix_tv = binary_matrix.corr()

    # Calling a function to return the dictionary of user genres
    user_genres = gal.get_anime_list_genres(anime_df, id_arr)
    sum = 0
    #determing the total number of genres in the dictionary
    for key in list(user_genres.keys()):
        sum += user_genres[key]
    for key in list(user_genres.keys()):

        if key in favorite_anime_genres:
            user_genres[key] += sum

        if key in str(favorite_anime_genres):
            user_genres[key] += round(sum*.65)

    sum = 0
    for key in list(user_genres.keys()):
        sum += user_genres[key]
    #adds the genre score to the dataframe based off of the weight of the user genres, 
    #calculated with the dictionary, and the genre coefficient
    def add_genre_score(genres): 
        count = 0
        target_anime_genres = genres.split(', ')
        for x in user_genres.keys():
            for y in target_anime_genres:
                #you can add the weight values in at this point by just multipling the value of corr_matrix_tv by the weight
                count += (corr_matrix_tv[x][y]*user_genres[x]/sum/1.1)
        return count

    anime_df['genre likeness'] = anime_df['Genres'].apply(add_genre_score)

    return anime_df