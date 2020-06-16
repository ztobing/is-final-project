import os
import numpy as np
import pandas as pd

class Predict:
    def __init__(self):
        DIR_PATH = os.path.dirname(os.path.realpath(__file__))
        MOST_POPULAR_PATH = DIR_PATH + "/models/most_popular.csv"
        COSINE_MATRIX_PATH = DIR_PATH + "/models/content_based.dat"
        COSINE_MATRIX_LEN_PATH = DIR_PATH + "/models/content_based_len.txt"
        MOVIES_METADATA_PATH = DIR_PATH + "/../datasets/movies_metadata.csv"

        self.MOVIES_METADATA = pd.read_csv(MOVIES_METADATA_PATH, low_memory=False)

        print("Loading cosine matrix data...")
        with open(COSINE_MATRIX_LEN_PATH) as file:
            self.COSINE_MATRIX_LEN = int(file.readline())
        self.COSINE_MATRIX = np.fromfile(COSINE_MATRIX_PATH).reshape((self.COSINE_MATRIX_LEN, self.COSINE_MATRIX_LEN))

        print("Loading most popular movies data...")
        self.MOST_POPULAR = pd.read_csv(MOST_POPULAR_PATH)
       
        print("Data loaded successfully.")


    def get_most_popular(self):
        return self.MOST_POPULAR.to_dict('records')

    def predict_content_based(self, movie_ids):
        recommend_list = []
        def get_similar_movies(movie_id):
            movie_index = self.MOVIES_METADATA.index[self.MOVIES_METADATA['id'] == movie_id].tolist()[0]
            similar_movies = list(enumerate(self.COSINE_MATRIX[movie_index]))
            similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
            similar_movies = similar_movies[1:11]

            def tuple_to_dict(tup, di):
                di = dict(tup) 
                return di
            similar_movies_dict = {}
            current_movie_title = self.MOVIES_METADATA.iloc[movie_index]["title"]
            return current_movie_title, tuple_to_dict(similar_movies, similar_movies_dict)

        for movie_id in movie_ids:
            current_movie_title, recommended_movies = get_similar_movies(movie_id)
            recommended_movies_metadata = []
            for recommended_movie in recommended_movies:
                # metadata = self.MOVIES_METADATA.loc[self.MOVIES_METADATA['id'] == str(recommended_movie)].to_dict()
                metadata = self.MOVIES_METADATA.iloc[recommended_movie].to_dict()
                recommended_movies_metadata.append(metadata)
            recommend_list.append({"movie_id": movie_id, "title": current_movie_title, "recommended": recommended_movies_metadata})

        return recommend_list

    def predict(self, ratings_list):
        # Temporarily only return most popular movies
        return self.get_most_popular()
