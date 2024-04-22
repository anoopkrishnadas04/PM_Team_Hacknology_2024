import requests
import numpy as np

import pandas as pd


def get_anime_list(username_input):
    CLIENT_ID = 'd3ec3d338e2dff3f68f91d8388258eb3'

    username = username_input

    x = 0
    flag = True

    id_arr = []

    while(flag):
        url = f'https://api.myanimelist.net/v2/users/{username}/animelist?fields=limit=1000&offset=' + str(x)
        #calling the MyAnimeList API
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })

        response.raise_for_status()
        anime = response.json()
        response.close()
        
        if(anime['data'] == []):
            flag = False
            break

        delim_str = '\n'

        if (x == 0):
            df = pd.json_normalize(anime['data'],
                        meta=[['node', 'id'],['node', 'title'],['node', 'main_picture'],
                                ['node', 'main_picture','medium'],['node', 'main_picture','large']])
            df.columns = ['id', 'title','medium image', 'large image']
            df = df.drop(['large image', 'medium image'],axis=1)
            f = open("output.txt", "w")
            for title in df['id']:
                f.write(str(title) + delim_str)
                id_arr.append(title)
            f.close()

        else:
            df_alt = pd.json_normalize( anime['data'],
                                        meta=[
                                        ['node', 'id'],
                                        ['node', 'title'],
                                        ['node', 'main_picture'],
                                        ['node', 'main_picture','medium'],
                                        ['node', 'main_picture','large']
                                        ])
            df_alt.columns = ['id', 'title','medium image', 'large image']
            df_alt = df_alt.drop(['large image', 'medium image'],axis=1)
            
            # Writes the list of id's
            f = open("output.txt", "a")
            for title in df_alt['id']:
                f.write(str(title) + delim_str)
                id_arr.append(title)
            f.close()


            df = pd.concat([df, df_alt], ignore_index=True)
        #print(x)
        x += 10
    # print(df)
    # print(df['title'])

    return id_arr


def get_anime_list_genres(id_arr):
    anime_df = pd.read_csv('anime-dataset-2023.csv')


    # Split genres and create a list of all genres excluding the specified ones
    anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]

    list(anime_df.columns)

    # print(anime_df[anime_df['anime_id'] == 2])

    anime_tv_list = list(anime_df['anime_id'])


    user_anime_genres = {
        "Action" : 0,
        "Award Winning" : 0,
        "Sci-Fi" : 0,
        "Adventure" : 0,
        "Drama" : 0,
        "Mystery" : 0,
        "Supernatural" : 0,
        "Fantasy" : 0,
        "Sports" : 0,
        "Comedy" : 0,
        "Romance" : 0,
        "Slice of Life" : 0,
        "Suspense" : 0,
        "Gourmet" : 0,
        "Avant Garde" : 0,
        "Horror" : 0,
        "Girls Love" : 0,
        "Boys Love" : 0,
        "UNKNOWN" : 0
    }

    x = 1

    #for anime_id in anime_df['anime_id'].items():
    #    print(anime_id)


    print(list(anime_df[anime_df['anime_id'] == 1]['Genres']))

    """
    for user_anime_id in id_arr:
        if user_anime_id in anime_tv_list:
            anime_df[anime_df['anime_id'] == user_anime_id]['Genres']
    """
    # print(type(anime_df['anime_id']))



get_anime_list_genres(get_anime_list("holesumname"))