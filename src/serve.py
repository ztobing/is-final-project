from flask import Flask, request, jsonify
from predict import Predict
from metadata import Metadata

# Initialize program
app = Flask(__name__)
metadata = Metadata()
predict = Predict()

@app.route('/')
def root():
    response = {"message": "Server is active"}
    return jsonify(response)

@app.route('/movie/<movie_id>')
def get_movie_by_id(movie_id):
    data = metadata.get_movie_by_id(int(movie_id)).to_dict()
    # response = {
    #     "adult": data[0],
    #     "imdbId": data[5],
    #     "originalLanguage": data[6],
    #     "title": data[-4],
    #     "overview": data[8],
    #     "releaseDate": data[-10]
    # }
    return jsonify(data)

@app.route('/recommend', methods=["GET", "POST"])
def get_most_popular():
    if request.method == "GET":
        data = predict.get_most_popular()
    else:
        data = {}
    
    return jsonify(data)

@app.route('/test-raw-data/<id>')
def test_function(id):
    response = {"value": predict.predict_content_based(int(id)).tolist()}
    return jsonify(response)
