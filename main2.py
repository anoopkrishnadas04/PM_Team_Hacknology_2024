import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity

#written (almost) entirely by Alex 
#this file is redundant but it shows the math that allowed us to create this project so it will remain
#in the repository as to show the though process that allowed us to determine what values to use
anime_df = pd.read_csv('anime-dataset-2023.csv')


# Split genres and create a list of all genres excluding the specified ones
anime_df = anime_df[~anime_df['Genres'].str.contains('Ecchi|Hentai|Erotica')]

list(anime_df.columns)

anime_df['Episodes'] = pd.to_numeric(anime_df['Episodes'], errors='coerce') #Converts all values from str -> float64
tv_anime_df = anime_df[anime_df['Type'] == 'TV'] #Include only TV data as to not skew results
#Determin median, mean, and range of Episodes
median_episodes_tv = tv_anime_df['Episodes'].median()
mean_episodes_tv = tv_anime_df['Episodes'].mean()
std_episodes_tv = tv_anime_df['Episodes'].std()
print(median_episodes_tv)
print(mean_episodes_tv)
print(std_episodes_tv)
#Create Box and whisker Plot of data Helps Visualize
plt.figure(figsize=(10, 6))
tv_anime_df.boxplot(column='Episodes', by='Type', grid=False, vert=False)
plt.xlabel('Type of Anime')
plt.ylabel('Number of Episodes')
plt.title('Box Plot of Number of Episodes by Type of Anime')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Determine median, mean, and range of Episodes to determine ranges and +/- values
tv_anime_df_low = tv_anime_df[tv_anime_df['Episodes'].isin(range(1, 26))]
median_episodes_tv_low = tv_anime_df_low['Episodes'].median()
mean_episodes_tv_low = tv_anime_df_low['Episodes'].mean()
std_episodes_tv_low = tv_anime_df_low['Episodes'].std()
print(median_episodes_tv_low)
print(mean_episodes_tv_low)
print(std_episodes_tv_low)
#Create box and whisker plot
tv_anime_df_low.boxplot(column='Episodes', by='Type', grid=False, vert=False)
plt.xlabel('Type of Anime')
plt.ylabel('Number of Episodes')
plt.title('Box Plot of Number of Episodes by Type of Anime')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Low:1-26 +5 (2 season shows)
#lowMedium:27-52  +/-7 (4 season shows)
#highMEdium:53-80 +-/8 (6 season shows)
#High:81+ (Arcs)


#Assign a score 1-4 according to the determined ranges to each show
def assign_episode_score(Episodes):
    if Episodes <= 26:
        return 1
    elif Episodes <= 52:
        return 2
    elif Episodes <= 80:
        return 3
    else:
        return 4

# Add new column 'episodeScore' based on 'episodes' column
tv_anime_df['episodeScore'] = tv_anime_df['Episodes'].apply(assign_episode_score)

# Display the updated DataFrame
tv_anime_df[['Name','Episodes', 'episodeScore']].dropna()


user_df = pd.read_csv('users-details-2023.csv')

user_df.head()

#Convert Values to Numeric
user_df['Completed'] = pd.to_numeric(user_df['Completed'], errors='coerce')
user_df['Watching'] = pd.to_numeric(user_df['Watching'], errors='coerce')
#Only include scores from people who have seen or are watching more than 0
user_df_alt = user_df[user_df['Completed']>0]
user_df_alt = user_df[user_df['Watching']>0]
#Calculate the mean median and std of the completed shows + shows they're watching
median_daysWatched= (user_df_alt['Completed'] + user_df_alt['Watching']).median()
mean_daysWatched = (user_df_alt['Completed']+ user_df_alt['Watching']).mean()
std_daysWatched= (user_df_alt['Completed'] + user_df_alt['Watching']).std()
print(median_daysWatched)
print(mean_daysWatched)
print(std_daysWatched)


# Calculate the user's score weights
user_df['userWeights'] = user_df.apply(lambda row: ((row['Watching'] + row['Completed']) / 61) if ((row['Watching'] + row['Completed']) / 100) < 0.5 else min(max((row['Watching'] + row['Completed']) / 100, 0.5), 2), axis=1)

# Print the updated DataFrame
user_df.head()

user_score_df = pd.read_csv('users-score-2023.csv')

user_score_df.head()

#***Only For TV shows
# Split genres and create a list of all genres excluding the specified ones
all_genres_tv = tv_anime_df['Genres'].str.split(', ').explode()

# Get unique genres
unique_genres_tv = all_genres_tv.unique()

# Display unique genres
print(unique_genres_tv)


# Assuming anime_df is your DataFrame with a column named 'Genres'

# Create a list of unique genres
genres_tv = tv_anime_df['Genres'].str.split(', ').explode().unique()

# Create a binary matrix where each row represents an anime and each column represents a genre
binary_matrix_tv = pd.DataFrame(columns=genres_tv)

for genre in genres_tv:
    binary_matrix_tv[genre] = tv_anime_df['Genres'].apply(lambda x: 1 if genre in x else 0)

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(binary_matrix_tv.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Genres')
plt.show()


#***For everything
# Split genres and create a list of all genres excluding the specified ones
all_genres = anime_df['Genres'].str.split(', ').explode()

# Get unique genres
unique_genres = all_genres.unique()

# Display unique genres
print(unique_genres)



# Assuming anime_df is your DataFrame with a column named 'Genres'

# Create a list of unique genres
genres = anime_df['Genres'].str.split(', ').explode().unique()

# Create a binary matrix where each row represents an anime and each column represents a genre
binary_matrix = pd.DataFrame(columns=genres)

for genre in genres:
    binary_matrix[genre] = anime_df['Genres'].apply(lambda x: 1 if genre in x else 0)

# Create a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(binary_matrix.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Genres')
plt.show()



# Assuming anime_df is your DataFrame with a column named 'Synopsis'

# Step 1: TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(anime_df['Synopsis'].values.astype('U'))  # Convert synopsis to Unicode

# Step 2: Calculate Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend similar anime based on title
def get_similar_anime(title, cosine_sim=cosine_sim):
    idx = anime_df[anime_df['Name'] == title].index[0]  # Get index of the anime
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar anime (excluding itself)
    anime_indices = [i[0] for i in sim_scores]
    return anime_df.iloc[anime_indices]

# Example usage:
similar_anime = get_similar_anime('One Piece')#One piece is a place holder
print(similar_anime[['Name', 'Synopsis']])


# Step 1: TF-IDF Vectorization
tfidf_vectorizer_tv = TfidfVectorizer(stop_words='english')
tfidf_matrix_tv= tfidf_vectorizer.fit_transform(tv_anime_df['Synopsis'].values.astype('U'))  # Convert synopsis to Unicode

# Step 2: Calculate Cosine Similarity
cosine_sim_tv = cosine_similarity(tfidf_matrix_tv, tfidf_matrix_tv)

# Function to recommend similar anime based on title
def get_similar_anime(title, cosine_sim=cosine_sim_tv):
    idx = tv_anime_df[tv_anime_df['Name'] == title].index[0]  # Get index of the anime
    sim_scores = list(enumerate(cosine_sim_tv[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 similar anime (excluding itself)
    anime_indices = [i[0] for i in sim_scores]
    return tv_anime_df.iloc[anime_indices]

# Example usage:
similar_anime = get_similar_anime('Bleach')#One piece is a place holder
print(similar_anime[['Name', 'Synopsis']])




# Preprocess the synopses
synopses_tv = tv_anime_df['Synopsis'].values.astype('U')  # Convert synopses to Unicode

# Tokenize the synopses
tokenized_synopses_tv = [synopsis.split() for synopsis in synopses_tv]

# Create a dictionary representation of the synopses
dictionary_tv = Dictionary(tokenized_synopses_tv)

# Filter out tokens that appear in less than 10 documents or more than 50% of the documents
dictionary_tv.filter_extremes(no_below=10, no_above=0.5)

# Convert the tokenized synopses into bag-of-words format
corpus_tv = [dictionary_tv.doc2bow(synopsis) for synopsis in tokenized_synopses_tv]

# Build the LDA model
lda_model_tv = LdaModel(corpus=corpus_tv,
                        id2word=dictionary_tv,
                        num_topics=5,  # Specify the number of topics
                        random_state=42,
                        passes=10)  # Number of passes through the corpus during training

# Function to preprocess user input
def preprocess_user_input(user_input_title, tv_anime_df):
    # Check if the user input matches any entry in the 'Name' column
    if user_input_title in tv_anime_df['Name'].values:
        return tv_anime_df.loc[tv_anime_df['Name'] == user_input_title, 'Synopsis'].values[0]
    # If not, check if the user input matches any entry in the 'English name' column
    elif user_input_title in tv_anime_df['English name'].values:
        return tv_anime_df.loc[tv_anime_df['English name'] == user_input_title, 'Synopsis'].values[0]
    # If neither 'Name' nor 'English name' matches, print "not in list"
    else:
        print("not in list")


# Get user input for the favorite TV show
user_favorite_title = input("Enter the title of your favorite TV show: ")

# Preprocess the user's favorite show synopsis
user_favorite_synopsis_tv = preprocess_user_input(user_favorite_title, tv_anime_df)

# Convert the user's favorite show synopsis into bag-of-words format
user_favorite_bow_tv = dictionary_tv.doc2bow(user_favorite_synopsis_tv.split())

# Get the topic distribution for the user's favorite show
user_favorite_topic_distribution_tv = lda_model_tv[user_favorite_bow_tv]

# Compute similarity between the user's show and other shows
index_tv = MatrixSimilarity(lda_model_tv[corpus_tv])
sims_tv = index_tv[user_favorite_topic_distribution_tv]

# Get the indices of the most similar shows
similar_show_indices_tv = sorted(enumerate(sims_tv), key=lambda item: -item[1])

# Recommend similar shows
# Exclude the user's favorite show from the recommended similar shows
similar_shows_tv = [(tv_anime_df.iloc[idx]['anime_id'], tv_anime_df.iloc[idx]['Name'], sim) for idx, sim in similar_show_indices_tv if tv_anime_df.iloc[idx]['Name'] != user_favorite_title]
i = 0
# Print the recommended similar shows line by line
for i, (show_id, show_name, similarity) in enumerate(similar_shows_tv[:10], start=1):  # Adjust the number of recommended shows as needed
    print(f"{i}. ID: {show_id}, Name: {show_name}, Similarity Score: {similarity}")


tv_anime_df[tv_anime_df['English name'] == "JoJo's Bizarre Adventure (2012)"]

# Filter the DataFrame for anime titles containing 'Jojo' in the 'Name' column
chr_search_anime = tv_anime_df[tv_anime_df['Name'].str.contains('Juju', case=False)]

# Print the filtered DataFrame
print(chr_search_anime)
