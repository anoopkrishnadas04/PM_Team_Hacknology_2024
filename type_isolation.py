import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.similarities import MatrixSimilarity

def update_df_by_type(anime_df, user_input):
    anime_df = anime_df[anime_df['Type'] == user_input] #Include only TV data as to not skew results
    return anime_df