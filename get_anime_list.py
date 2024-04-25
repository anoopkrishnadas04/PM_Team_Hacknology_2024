import requests
import numpy as np

import pandas as pd

import json


def get_anime_list(username_input):
    CLIENT_ID = 'd3ec3d338e2dff3f68f91d8388258eb3'

    username = username_input

    x = 0
    flag = True

    id_arr = []

    while(flag):
        url = f'https://api.myanimelist.net/v2/users/{username}/animelist?fields=limit=1000&sort=list_score&status=watching&status=completed&offset=' + str(x)
        #calling the MyAnimeList API
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })
        try:
            response.raise_for_status()
            anime = response.json()
            response.close()
        #verifying that the API call has suceeded
        except requests.exceptions.HTTPError as errh:
            username = input('please try to re-type your username, or enter another: ')
            continue
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)
        
        #determining if we have finished returning the users anime list due to pagination
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

        x += 10

    return id_arr


def get_anime_list_genres(anime_df, id_arr):

    # Split genres and create a list of all genres excluding the specified ones
    anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]

    list(anime_df.columns)

    # print(anime_df[anime_df['anime_id'] == 2])

    anime_tv_list = list(anime_df['anime_id'])


    total_user_anime_genres = {
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
    
    for user_anime_id in id_arr:
        if user_anime_id in anime_tv_list:
            for user_anime_genre in str(list(anime_df[anime_df['anime_id'] == user_anime_id]['Genres'])[0]).split(", "):
                total_user_anime_genres[user_anime_genre] += 1
    

    sum = 0
    for key in list(total_user_anime_genres.keys()):
        sum += total_user_anime_genres[key]


    return total_user_anime_genres

def get_dropped_anime_list(username_input):
    CLIENT_ID = 'd3ec3d338e2dff3f68f91d8388258eb3'

    username = username_input

    x = 0
    flag = True

    id_arr = []

    while(flag):
        url = f'https://api.myanimelist.net/v2/users/{username}/animelist?fields=limit=1000&sort=list_score&status=dropped&offset=' + str(x)
        #calling the MyAnimeList API
        response = requests.get(url, headers = {
            'X-MAL-CLIENT-ID': CLIENT_ID
        })
        try:
            response.raise_for_status()
            anime = response.json()
            response.close()
        #verifying that the API call has suceeded
        except requests.exceptions.HTTPError as errh:
            username = input('please try to re-type your username, or enter another: ')
            continue
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)
        
        #determining if we have finished returning the users anime list due to pagination
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

        x += 10

    return id_arr