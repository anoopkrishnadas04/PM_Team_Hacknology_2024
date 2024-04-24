import pandas as pd
import type_isolation as t
import genre_likeness as gl
import get_anime_list as gal
import length_preference as lp

###########################################################
#create the dataframe based off of the csv
anime_df = pd.read_csv('anime-dataset-2023.csv')
#filter out NSFW shows
anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]
print("Reading the dataframe")

###########################################################
#Assign a score 1-4 according to the determined ranges to each show
anime_df['Episodes'] = pd.to_numeric(anime_df['Episodes'], errors='coerce') #Converts all values from str -> float64
def assign_episode_score(Episodes):
    if Episodes == 1:
        return 1
    elif Episodes <= 26:
        return 2
    elif Episodes <= 52:
        return 3
    elif Episodes <= 80:
        return 4
    else:
        return 5

# Add new column 'episodeScore' based on 'episodes' column
anime_df['episodeScore'] = anime_df['Episodes'].apply(assign_episode_score)
print("assigned length scores")

#####################################
#create a dataframe based off of the user csv
user_df = pd.read_csv('users-details-2023.csv')
user_score_df = pd.read_csv('users-score-2023.csv')

#####################################
#add a new score based off of user exclusion chocies
user_df['Mean Score'].isnull().sum()

# If there are null values, handle them by replacing them with a specific value (e.g., 0)
user_df['Mean Score'].fillna(0, inplace=True)

# Convert Values to Numeric
user_df['Completed'] = pd.to_numeric(user_df['Completed'], errors='coerce')
user_df['Watching'] = pd.to_numeric(user_df['Watching'], errors='coerce')
user_df['Mean Score'] = pd.to_numeric(user_df['Mean Score'], errors='coerce')


# Filter out users with total completed+watching < 25
user_df_alt= user_df[(user_df['Completed'] + user_df['Watching']) >= 25]
user_df_alt = user_df_alt[(user_df_alt['Mean Score'] < 8.5) & (user_df_alt['Mean Score'] > 2.5)]

merged_df = pd.merge(user_score_df, user_df_alt, left_on='user_id', right_on='Mal ID')
# Calculate average scores for anime
anime_avg_scores = merged_df.groupby('anime_id')['rating'].agg(['mean', 'count']).reset_index()

# Merge anime_avg_scores with anime_df to add the new column
anime_df = pd.merge(anime_df, anime_avg_scores, on='anime_id', how='left')
anime_df.rename(columns={'mean': 'newScore', 'count': 'rating_count'}, inplace=True)

# Replace newScore with original score for shows with less than 20 ratings
anime_df.loc[anime_df['rating_count'] < 20, 'newScore'] = anime_df.loc[anime_df['rating_count'] < 20, 'Score']

# Drop the rating_count column
anime_df.drop('rating_count', axis=1, inplace=True)
anime_df['newScore'] = anime_df['newScore'].fillna(0)
anime_df['newScore'] = pd.to_numeric(anime_df['newScore'], errors='coerce')
print("calculated new scores")
anime_df.to_csv('updated-anime-dataset-2023.csv', index=False)