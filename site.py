from flask import Flask, Response
from flask_cors import CORS, cross_origin
from flights import Cphdk
import json

app = Flask(__name__)
CORS(app)
Cph = Cphdk()

@app.route('/api/departures/')
def departures():
    return Response(
        json.dumps(Cph.parse_departure_table()), mimetype='application/json')

@app.route('/api/arrivals/')
def arrivals():
    return Response(
        json.dumps(Cph.parse_arrival_table()), mimetype='application/json')

if __name__ == '__main__':
    app.run()
