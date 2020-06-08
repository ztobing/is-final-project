import os, csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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

q_movies.to_csv(MODELS_PATH + "/most_popular.csv")
print("Most popular movies list is saved to /models/most_popular.csv")

#
# Create Content-based Filtering Model
#
print("--- Creating content-based model ---")

# Fill N/A overview fields with empty string
print("Cleaning movies metadata column...")
MOVIES_METADATA["overview"] = MOVIES_METADATA["overview"].fillna("")

# Vectorize movie overview
print("Generating vectorized movies overview...")
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(MOVIES_METADATA["overview"])

# Calculate cosine similarity matrix for each movies in the database
print("Calculating cosine similarity matrix...")
cosine_similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)

# Save the cosine similarity matrix as file
print("Saving matrix to as raw data...")
cosine_similarity_matrix.tofile(MODELS_PATH + "/content_based.dat")
with open(MODELS_PATH + "/content_based_len.txt", "w") as file:
    file.write(str(len(cosine_similarity_matrix)))
print("Content-based model saved to model/content_based.dat and model/content_based_len.txt")

#
# Create Collaborative Filtering Model
#
