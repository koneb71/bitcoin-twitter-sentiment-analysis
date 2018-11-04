import os
from flask import Flask, jsonify, request
from db import *
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hSlwSo23OXksd#$jsnFMSl92382'

CORS(app)


@app.route("/sentiment/data/bitcoin")
def data():
    data = get_graph_data("bitcoin")
    return jsonify({'positive': [item['positive'] for item in data],
                    'negative': [item['negative'] for item in data],
                    'bitcoin_price': [item['bitcoin_price'] for item in data],
                    'timestamp': [item['timestamp'] for item in data]
                    })


if __name__ == '__main__':
    app.run(debug=True)
