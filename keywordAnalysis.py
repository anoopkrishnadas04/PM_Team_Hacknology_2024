import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity
def keyword_analysis(pop_df, anime_df):
    anime_df = pd.read_csv('updated-anime-dataset-2023.csv')
    pop_df = pop_df
    # Preprocess the synopses
    synopses_tv = pop_df['Synopsis'].values.astype('U')  # Convert synopses to Unicode

    # Tokenize the synopses
    tokenized_synopses_tv = [synopsis.split() for synopsis in synopses_tv]

    # Create a dictionary representation of the synopses
    dictionary_tv = Dictionary(tokenized_synopses_tv)

    # Filter out tokens that appear in less than 10 documents or more than 50% of the documents
    dictionary_tv.filter_extremes(no_below=10, no_above=0.5)

    # Convert the tokenized synopses into bag-of-words format
    corpus_tv = [dictionary_tv.doc2bow(synopsis) for synopsis in tokenized_synopses_tv]
    print("beginning analysis")

    # Build the LDA model
    lda_model_tv = LdaModel(corpus=corpus_tv,
                            id2word=dictionary_tv,
                            num_topics= 5,  # Specify the number of topics
                            random_state=42,
                            passes=10)  # Number of passes through the corpus during training

    # Function to preprocess user input
    def preprocess_user_input(user_input_title, pop_df):
        # Check if the user input matches any entry in the 'Name' column
        if user_input_title in anime_df['Name'].values:
            return anime_df.loc[anime_df['Name'] == user_input_title, 'Synopsis'].values[0]
        # If not, check if the user input matches any entry in the 'English name' column
        elif user_input_title in anime_df['English name'].values:
            return anime_df.loc[anime_df['English name'] == user_input_title, 'Synopsis'].values[0]
        # If neither 'Name' nor 'English name' matches, print "not in list"
        else:
            print("not in list")

    def get_anime_id(show_name):
        if show_name in anime_df['Name'].values:
            row = anime_df.loc[anime_df['Name'] == show_name]
            return row.iloc[0]['anime_id']
        elif show_name in anime_df['English name'].values:
            row = anime_df.loc[anime_df['English name'] == show_name]
            return row.iloc[0]['anime_id']
        else:
            return None




    # Get user input for the favorite TV show
    user_favorite_title = input("Enter the title of your favorite TV show: ")

    while(get_anime_id(user_favorite_title) == None):
        user_favorite_title = input("Please try again: ")
    # Get the anime_id of the user's favorite show
    anime_id = get_anime_id(user_favorite_title)

    # Check if the user's favorite show is in pop_df
    if anime_id in pop_df['anime_id'].values:
        user_favorite_index = pop_df.index[pop_df['anime_id'] == anime_id][0]  # Get the index of the user's favorite show in pop_df
        user_favorite_title = pop_df.loc[user_favorite_index, 'Name']  # Get the name of the user's favorite show in pop_df

    # Preprocess the user's favorite show synopsis
 
    user_favorite_synopsis_tv = preprocess_user_input(user_favorite_title, anime_df)

    # Convert the user's favorite show synopsis into bag-of-words format
    user_favorite_bow_tv = dictionary_tv.doc2bow(user_favorite_synopsis_tv.split())

    # Get the topic distribution for the user's favorite show
    user_favorite_topic_distribution_tv = lda_model_tv[user_favorite_bow_tv]

    # Compute similarity between the user's show and other shows
    index_tv = MatrixSimilarity(lda_model_tv[corpus_tv])
    sims_tv = index_tv[user_favorite_topic_distribution_tv]

     # Add similarity scores to pop_df
    pop_df['keywordScore'] = sims_tv

    # Sort pop_df by similarity scores
    #pop_df = pop_df.sort_values(by='keywordScore', ascending=False)

    
    return pop_df
   