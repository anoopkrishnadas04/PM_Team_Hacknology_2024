import pandas as pd
import numpy as np

def apply_length_difference(anime_df, id_arr):
    anime_list = list(anime_df['anime_id'])
    sum = 0
    count = 0
    for anime_id in id_arr:
        if anime_id in anime_list:
            count += 1
            foo = list(anime_df[anime_df['anime_id'] == anime_id]['episodeScore'])[0]
            sum += foo
    sum = round(sum/count)
    def calc_score_difference(score):
        score = abs(int(score) - sum)
        return 1 - (score/4)/11
    anime_df['lengthLikeness'] = anime_df['episodeScore'].apply(calc_score_difference)
    return anime_df


    