import os
import numpy as np
import pandas as pd

class Predict:
    def __init__(self):
        DIR_PATH = os.path.dirname(os.path.realpath(__file__))
        MOST_POPULAR_PATH = DIR_PATH + "/models/most_popular.csv"
        COSINE_MATRIX_PATH = DIR_PATH + "/models/content_based.dat"
        COSINE_MATRIX_LEN_PATH = DIR_PATH + "/models/content_based_len.txt"

        print("Loading cosine matrix data...")
        with open(COSINE_MATRIX_LEN_PATH) as file:
            self.COSINE_MATRIX_LEN = int(file.readline())
        self.COSINE_MATRIX = np.fromfile(COSINE_MATRIX_PATH).reshape((self.COSINE_MATRIX_LEN, self.COSINE_MATRIX_LEN))

        print("Loading most popular movies data...")
        self.MOST_POPULAR = pd.read_csv(MOST_POPULAR_PATH)
        
        print("Data loaded successfully.")


    def get_most_popular(self):
        return self.MOST_POPULAR.to_dict('records')

    def predict_content_based(self, movie_id):
        return self.COSINE_MATRIX[movie_id]

    def predict(self, ratings_list):
        # Temporarily only return most popular movies
        return self.get_most_popular()