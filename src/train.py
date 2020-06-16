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
print(len(MOVIES_METADATA))



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
credits = pd.read_csv(DIR_PATH + '/../datasets/credits.csv')
keywords = pd.read_csv(DIR_PATH + '/../datasets/keywords.csv')

# Remove rows with bad IDs.
MOVIES_METADATA = MOVIES_METADATA.drop([19730, 29503, 35587])
print(len(MOVIES_METADATA))

# Convert IDs to int. Required for merging
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
MOVIES_METADATA['id'] = MOVIES_METADATA['id'].astype('int')
print(len(MOVIES_METADATA))

# Merge keywords and credits into your main metadata dataframe
MOVIES_METADATA = MOVIES_METADATA.merge(credits, on='id')
MOVIES_METADATA = MOVIES_METADATA.merge(keywords, on='id')

print(len(MOVIES_METADATA))

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
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

MOVIES_METADATA['director'] = MOVIES_METADATA['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    MOVIES_METADATA[feature] = MOVIES_METADATA[feature].apply(get_list)

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    MOVIES_METADATA[feature] = MOVIES_METADATA[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

MOVIES_METADATA['soup'] = MOVIES_METADATA.apply(create_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(MOVIES_METADATA['soup'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)


# Save the cosine similarity matrix as file
print("Saving matrix to as raw data...")
cosine_sim.tofile(MODELS_PATH + "/content_based.dat")
with open(MODELS_PATH + "/content_based_len.txt", "w") as file:
    file.write(str(len(cosine_sim)))
print("Content-based model saved to model/content_based.dat and model/content_based_len.txt")





def get_recommendations(title, cosine_sim):
    # Get the index of the movie that matches the title
    indices = pd.Series(MOVIES_METADATA.index, index=MOVIES_METADATA['title'])
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:10]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return MOVIES_METADATA['title'].iloc[movie_indices]

print (get_recommendations('The Dark Knight Rises', cosine_sim))

