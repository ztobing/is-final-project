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
print("Saving matrix to csv...")
# pd.DataFrame(cosine_similarity_matrix).to_csv(MODELS_PATH + "/content_based.csv")
cosine_similarity_matrix.tofile(MODELS_PATH + "/content_based.dat")
# with open(MODELS_PATH + "/content_based.csv", "wb") as file:
#     wr = csv.writer(file, quoting=csv.QUOTE_ALL)
#     wr.writerows(cosine_similarity_matrix)
print("Content-based model saved to model/content_based.dat")

#
# Create Collaborative Filtering Model
#
