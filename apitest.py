import requests
import numpy as np

import pandas as pd

CLIENT_ID = 'd3ec3d338e2dff3f68f91d8388258eb3'

url = 'https://api.myanimelist.net/v2/users/holesumname/animelist?fields=limit=1000&offset=0'
#calling the MyAnimeList API
response = requests.get(url, headers = {
    'X-MAL-CLIENT-ID': CLIENT_ID
    })

response.raise_for_status()
anime = response.json()
response.close()

#turning the JSON response into a pandas data frame
df = pd.json_normalize(anime['data'],
                       meta=[['node', 'id'],['node', 'title'],['node', 'main_picture'],
                             ['node', 'main_picture','medium'],['node', 'main_picture','large']])
df.columns = ['id', 'title','medium image', 'large image']
x = 10
flag = True
while(flag):
    url = 'https://api.myanimelist.net/v2/users/TheYellowInvader/animelist?fields=limit=1000&offset=' + str(x)
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
    df_alt = pd.json_normalize(anime['data'],
                       meta=[['node', 'id'],['node', 'title'],['node', 'main_picture'],
                             ['node', 'main_picture','medium'],['node', 'main_picture','large']])
    df_alt.columns = ['id', 'title','medium image', 'large image']
    df = pd.concat([df, df_alt])
    x += 10
print(df)

