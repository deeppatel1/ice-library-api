from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from get_details import get_details
from search import search_elastic
from constants import ElasticConstants
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


client = Elasticsearch(ElasticConstants.ELASTICSEARCH_HOST)


@app.route('/<video_id>', methods=['GET'])
def get_video_details(video_id):
    response = jsonify(get_details(client, video_id))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    response = jsonify(search_elastic(client, query))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
if __name__ == "__main__":
    app.run(debug=False)