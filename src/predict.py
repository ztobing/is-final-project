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
        credits = pd.read_csv(DIR_PATH + '/../datasets/credits.csv')
        keywords = pd.read_csv(DIR_PATH + '/../datasets/keywords.csv')
        self.MOVIES_METADATA = pd.read_csv(MOVIES_METADATA_PATH, low_memory=False).drop(columns=['adult', 'belongs_to_collection', 
                                                                    'genres', 'homepage', 'budget',
                                                                    'original_language',
                                                                    'original_title', 'overview',
                                                                    'popularity', 'production_companies',
                                                                    'production_countries', 'release_date',
                                                                    'revenue', 'runtime', 'spoken_languages',
                                                                    'video', 'tagline', 'vote_average',
                                                                    'vote_count', 'imdb_id', 'status'
                                                                   ], axis=1)
        self.MOVIES_METADATA = self.MOVIES_METADATA.drop([19730, 29503, 35587])

        keywords['id'] = keywords['id'].astype('int')
        credits['id'] = credits['id'].astype('int')

        self.MOVIES_METADATA['id'] = self.MOVIES_METADATA['id'].astype('int')
        print(len(self.MOVIES_METADATA))

        # Merge keywords and credits into your main metadata dataframe
        self.MOVIES_METADATA = self.MOVIES_METADATA.merge(credits, on='id')
        self.MOVIES_METADATA = self.MOVIES_METADATA.merge(keywords, on='id')

        self.MOVIES_METADATA['id'] = self.MOVIES_METADATA['id'].astype('int')
        # self.MOVIES_METADATA['imdb_id'] = self.MOVIES_METADATA['imdb_id'].astype('int')

        # self.MOVIES_METADATA['budget'].fillna(0, inplace=True)
        # self.MOVIES_METADATA['budget'] = self.MOVIES_METADATA['budget'].astype('int')
        # self.MOVIES_METADATA['popularity'] = self.MOVIES_METADATA['popularity'].astype('int')
        # self.MOVIES_METADATA['revenue'].fillna(0, inplace=True)
        # self.MOVIES_METADATA['revenue'] = self.MOVIES_METADATA['revenue'].astype('int')

        # self.MOVIES_METADATA['vote_count'].fillna(0, inplace=True)
        # self.MOVIES_METADATA['vote_count'] = self.MOVIES_METADATA['vote_count'].astype('int')

        # self.MOVIES_METADATA['runtime'].fillna(0, inplace=True)
        # self.MOVIES_METADATA['runtime'] = self.MOVIES_METADATA['runtime'].astype('int')
        # self.MOVIES_METADATA['vote_average'] = self.MOVIES_METADATA['vote_average'].astype('int')
        # self.MOVIES_METADATA['vote_count'] = self.MOVIES_METADATA['vote_count'].astype('int')

        print("Loading cosine matrix data...")
        with open(COSINE_MATRIX_LEN_PATH) as file:
            self.COSINE_MATRIX_LEN = int(file.readline())
        self.COSINE_MATRIX = np.fromfile(COSINE_MATRIX_PATH).reshape((self.COSINE_MATRIX_LEN, self.COSINE_MATRIX_LEN))

        print("Loading most popular movies data...")
        self.MOST_POPULAR = pd.read_csv(MOST_POPULAR_PATH)
       
        print("Data loaded successfully.")

    def get_recommendations(self, title):
        # Get the index of the movie that matches the title
        indices = pd.Series(self.MOVIES_METADATA.index, index=self.MOVIES_METADATA['title'])
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.COSINE_MATRIX[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return self.MOVIES_METADATA['title'].iloc[movie_indices]

    def get_most_popular(self):
        return self.MOST_POPULAR.to_dict('records')

    def predict_content_based(self, movie_ids):
        recommend_list = []
        def get_similar_movies(movie_id):
            print("Getting recommendations for", movie_id)
            movie_index = self.MOVIES_METADATA.index[self.MOVIES_METADATA['id'] == int(movie_id)].tolist()[0]
            similar_movies = list(enumerate(self.COSINE_MATRIX[movie_index]))
            similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
            similar_movies = similar_movies[1:11]

            def tuple_to_dict(tup, di):
                di = dict(tup) 
                return di
            similar_movies_dict = {}
            current_movie_title = self.MOVIES_METADATA.iloc[movie_index]["title"]
            print(movie_id,similar_movies_dict)
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
