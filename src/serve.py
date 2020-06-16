from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import urllib
from predict import Predict
from metadata import Metadata
import numpy as np
import json

# Initialize program
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
metadata = Metadata()
predict = Predict()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

@app.route('/')
@cross_origin()
def root():
    response = {"message": "Server is active"}
    return jsonify(response)

@app.route('/movie/<movie_id>')
@cross_origin()
def get_movie_by_id(movie_id):
    data = metadata.get_movie_by_id(int(movie_id)).to_dict()
    return jsonify(data)

@app.route('/search-movie-name/<movie_name>')
@cross_origin()
def get_movie_by_name(movie_name):
    data = metadata.get_movie_by_title(urllib.parse.unquote(movie_name))
    return jsonify(data)

@app.route('/recommend', methods=["GET", "POST"])
@cross_origin()
def get_recommendation():
    if request.method == "GET":
        data = {"all-time-popular": predict.get_most_popular()}
    else:
        ratings = request.get_json()
        data = {
            "all-time-popular": predict.get_most_popular(),
            "content-based": predict.predict_content_based({k: v for k, v in ratings.items() if int(v) >= 4})
        }
    return json.dumps(data, cls=NpEncoder)
    # return jsonify(data)
