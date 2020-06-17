import os, csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MOVIES_METADATA_PATH = DIR_PATH + "/../datasets/movies_metadata.csv"
RATINGS_METADATA_PATH = DIR_PATH + "/../datasets/ratings.csv"
MODELS_PATH = DIR_PATH + "/models"
MOVIES_METADATA = pd.read_csv(MOVIES_METADATA_PATH, low_memory=False)

#
# Load top rated movies
#
print("Calculating most popular movies...")

rating_mean = MOVIES_METADATA['vote_average'].mean()
most_voted_movies_count = MOVIES_METADATA['vote_count'].quantile(0.90)
q_movies = MOVIES_METADATA.copy().loc[MOVIES_METADATA['vote_count'] >= most_voted_movies_count]
def weighted_rating(x, m=most_voted_movies_count, C=rating_mean):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)
q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
q_movies = q_movies.sort_values('score', ascending=False)

q_movies.head(50).to_csv(MODELS_PATH + "/most_popular.csv")
print("Most popular movies list is saved to /models/most_popular.csv")

#
# Create Content-based Filtering Model
#
print("--- Creating content-based model ---")

# Load keywords and credits
CREDITS = pd.read_csv(DIR_PATH + '/../datasets/credits.csv')
KEYWORDS = pd.read_csv(DIR_PATH + '/../datasets/keywords.csv')

# Remove rows with bad IDs.
MOVIES_METADATA = MOVIES_METADATA.drop([19730, 29503, 35587])

# Convert IDs to int. Required for merging
KEYWORDS['id'] = KEYWORDS['id'].astype('int')
CREDITS['id'] = CREDITS['id'].astype('int')
MOVIES_METADATA['id'] = MOVIES_METADATA['id'].astype('int')

# Merge keywords and credits into your main metadata dataframe
MOVIES_METADATA = MOVIES_METADATA.merge(CREDITS, on='id')
MOVIES_METADATA = MOVIES_METADATA.merge(KEYWORDS, on='id')


features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    MOVIES_METADATA[feature] = MOVIES_METADATA[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

MOVIES_METADATA['soup'] = MOVIES_METADATA.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(MOVIES_METADATA['soup'])

COSINE_SIMILARITY_MATRIX = cosine_similarity(count_matrix, count_matrix)


# Save the cosine similarity matrix as file
print("Saving matrix to as raw data...")
COSINE_SIMILARITY_MATRIX.tofile(MODELS_PATH + "/content_based.dat")
with open(MODELS_PATH + "/content_based_len.txt", "w") as file:
    file.write(str(len(COSINE_SIMILARITY_MATRIX)))
print("Content-based model saved to model/content_based.dat and model/content_based_len.txt")