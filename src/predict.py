import os
import numpy as np

class Predict:
    def __init__(self):
        DIR_PATH = os.path.dirname(os.path.realpath(__file__))
        COSINE_MATRIX_PATH = DIR_PATH + "/models/content_based.dat"
        COSINE_MATRIX_LEN_PATH = DIR_PATH + "/models/content_based_len.txt"

        print("Loading matrix data...")
        with open(COSINE_MATRIX_LEN_PATH) as file:
            self.COSINE_MATRIX_LEN = int(file.readline())
        self.COSINE_MATRIX = np.fromfile(COSINE_MATRIX_PATH).reshape((self.COSINE_MATRIX_LEN, self.COSINE_MATRIX_LEN))

    def predictContentBased(self, movie_id):
        print(self.COSINE_MATRIX[movie_id])
