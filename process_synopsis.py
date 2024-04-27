import pandas as pd
import re
import type_isolation as t
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag
import pickle

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
stopwords = set(stopwords.words('english'))

def process_synopsis(pop_df):
    #opening the original dataset as for processing purposes the original dataframe has filtered out
    #all shows the user has already watched, which would make it impossible to access synopsis of 
    #users favorite show
    #solves a random error
    pop_df = pop_df

    user_input = 'TV'
    pop_df = t.update_df_by_type(pop_df, user_input)

    # Preprocess the synopses
    synopses_tv = pop_df['Synopsis'].values.astype('U')  # Convert synopses to Unicode

    # Tokenize the synopses
    tokenized_synopses_tv = [synopsis.split() for synopsis in synopses_tv]

    tokenized_synopses_no_stopwords = [[token for token in synopsis if token.lower() not in stopwords] for synopsis in tokenized_synopses_tv]

    # POS Tagging
    tokenized_synopses_pos = [pos_tag(tokens) for tokens in tokenized_synopses_no_stopwords]
    
    # Keep tokens that are nouns, verbs, adjectives, and adverbs
    allowed_pos = {'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'}
    tokenized_synopses_filtered = [[token for token, pos in tagged_tokens if pos in allowed_pos] for tagged_tokens in tokenized_synopses_pos]
    
    # Remove tokens that are too short or too long
    tokenized_synopses_filtered = [[token for token in synopsis if 2 <= len(token) <= 15] for synopsis in tokenized_synopses_filtered]
    
    # Remove tokens containing non-alphabetical characters or digits
    tokenized_synopses_filtered = [[token for token in synopsis if token.isalpha()] for synopsis in tokenized_synopses_filtered]
    
    # Create a dictionary representation of the synopses
    dictionary_tv = Dictionary(tokenized_synopses_filtered)

    # Filter out tokens that appear in less than 10 documents or more than 50% of the documents
    dictionary_tv.filter_extremes(no_below=10, no_above=0.5)

    dictionary_tv.save_as_text("synopDict.txt")

    with open('synopses_no_stopwords.ob', 'wb') as fp:
        pickle.dump(tokenized_synopses_no_stopwords, fp)

