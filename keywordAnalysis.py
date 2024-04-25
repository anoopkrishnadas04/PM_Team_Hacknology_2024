import pandas as pd
import re
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity

def get_anime_id(anime_df,show_name):
        flag = True
        while flag:
            #turning the show name into regex pattern
            show_name_pattern = re.escape(show_name.lower())
            regex_pattern = re.compile(show_name_pattern, re.IGNORECASE)
            #creating filters for regex pattern
            matches_english = anime_df['English name'].str.contains(regex_pattern, na=False)
            matches = anime_df['Name'].str.contains(regex_pattern, na=False)
            #if user inputs name exactly this will run
            if show_name in anime_df['Name'].values:
                row = anime_df.loc[anime_df['Name'] == show_name]
                return row.iloc[0]['anime_id']
            #if user inputs english name exactly this will run
            elif show_name in anime_df['English name'].values:
                row = anime_df.loc[anime_df['English name'] == show_name]
                return row.iloc[0]['anime_id']
            #if user inputs a partial match to any name this will run and verify the name
            elif anime_df['Name'].str.contains(regex_pattern, na=False).any():
                filter_anime_df = anime_df[matches]
                if not filter_anime_df.empty:
                    print(filter_anime_df.iloc[0]['Name'])
                    if input("is this the anime you were searching for? (y/n): ").lower() == 'y':
                        print("That's great, we'll continue analyzing then")
                    else:
                        show_name = input("Sorry about that, please try to enter it more accurately: ")
                        continue
                    return filter_anime_df.iloc[0]['anime_id']
                show_name = input("That name didn't come up in our list, please try again: ")
                continue
            #if user inputs a partial match to any english name this will run and verify the name
            elif anime_df['English name'].str.contains(regex_pattern, na=False).any():
                filter_anime_df = anime_df[matches_english]
                if not filter_anime_df.empty:
                    if input("is this the anime you were searching for? (y/n): ").lower() == 'y':
                        print("That's great, we'll continue analyzing then")
                    else:
                        show_name = input("Sorry about that, please try to enter it more accurately: ")
                        continue
                    return filter_anime_df.iloc[0]['anime_id']
                show_name = input("That name didn't come up in our list, please try again: ")
                continue
            else:
                show_name = input("That name didn't come up in our list, please try again: ")
                continue

def keyword_analysis(pop_df, anime_df, anime_id):
    #opening the original dataset as for processing purposes the original dataframe has filtered out
    #all shows the user has already watched, which would make it impossible to access synopsis of 
    #users favorite show
    anime_df = pd.read_csv('updated-anime-dataset-2023.csv')
    #solves a random error
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
                            num_topics= 5,  # Specify the number of topics Default val = 5
                            random_state=42,
                            passes= 10)  # Number of passes through the corpus during training default val=10

    # Function to preprocess user input - redundant- I would like to remove this function
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

    




    # Get user input for the favorite TV show#################################################
    #user_favorite_title = input("Enter the title of your favorite TV show: ")################
##############################################################################################
    #anime_id = get_anime_id(user_favorite_title)#############################################

    # Check if the user's favorite show is in pop_df - redundant, would like to remove
    if anime_id in pop_df['anime_id'].values:
        user_favorite_index = pop_df.index[pop_df['anime_id'] == anime_id][0]  # Get the index of the user's favorite show in pop_df
        user_favorite_title = pop_df.loc[user_favorite_index, 'Name']  # Get the name of the user's favorite show in pop_df

    # Preprocess the user's favorite show synopsis
 
    user_favorite_synopsis_tv = anime_df.loc[anime_df['anime_id'] == anime_id, 'Synopsis'].values[0]

    # Convert the user's favorite show synopsis into bag-of-words format
    user_favorite_bow_tv = dictionary_tv.doc2bow(user_favorite_synopsis_tv.split())

    # Get the topic distribution for the user's favorite show
    user_favorite_topic_distribution_tv = lda_model_tv[user_favorite_bow_tv]

    # Compute similarity between the user's show and other shows
    index_tv = MatrixSimilarity(lda_model_tv[corpus_tv])
    sims_tv = index_tv[user_favorite_topic_distribution_tv]

     # Add similarity scores to pop_df
    pop_df['keywordScore'] = sims_tv

    
    return pop_df
   