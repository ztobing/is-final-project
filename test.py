import pandas as pd

from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import TfidVectorizer


credits = pd.read_csv("credits.csv")
credits.head()

movies = pd.read_csv("movies_metadata.csv")
movies.head()

print("Credits: ", credits.shape)
print("Movies: ", movies.shape)

# moviesMerge = movies.merge(credits, on = "id")
# moviesMerge.head()

moviesSorted = movies.drop(columns = ["homepage", "production_countries", "status"])
moviesSorted.info()
# moviesSorted.head(1)["overview"]


tfv = TfidVectorizer(min_df = 3, maxFeatures = None, stripAccents = "unicode", analyzer = "word", tokenPattern =r"\w{1,}", ngramRange = (1, 3), stopWords = "english")

moviesSorted["overview"] = movies["overview"].fillna("")

tfvMatrix = tfv.fit_transform(moviesSorted["overview"])
tfvMatrix
tfvMatrix.shape

sig = sigmoid_kernel(tfvMartrix, tfvMatrix)
sig[0]

indices = pd.Series()(moviesSorted.index, index = moviesSorted["original_title"]).drop_duplicates()
indices

def giveRec(title, sig = sig):
    idx = indices[title]
    sigScore = list(enumerate(sig[idx]))
    sigScore = sored(sigScore, key = lambda x: x[1], reverse = TruesigScore)
    sigScore = sigScore[1:11]
    movieIndices = [i[0] for i in sigScore]
    return moviesSorted["original_title"].iloc[movieIndices]

giveRec("Spy Kids")