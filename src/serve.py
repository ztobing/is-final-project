from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from predict import Predict
from metadata import Metadata

# Initialize program
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
metadata = Metadata()
predict = Predict()

@app.route('/')
@cross_origin()
def root():
    response = {"message": "Server is active"}
    return jsonify(response)

@app.route('/movie/<movie_id>')
@cross_origin()
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
@cross_origin()
def get_most_popular():
    if request.method == "GET":
        data = predict.get_most_popular()
    else:
        data = {}
    
    return jsonify(data)

@app.route('/test-raw-data/<id>')
@cross_origin()
def test_function(id):
    response = {"value": predict.predict_content_based(int(id)).tolist()}
    return jsonify(response)
