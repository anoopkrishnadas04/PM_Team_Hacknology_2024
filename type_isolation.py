import pandas as pd
import numpy as np


def update_df_by_type(anime_df, user_input):
    anime_df = anime_df[anime_df['Type'] == user_input] #Include only TV data as to not skew results
    return anime_df