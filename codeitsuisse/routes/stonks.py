import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def get_id():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for _ in data:
        energy = data.get("energy")
        capital = data.get("capital")
        timeline = data.get("timeline")
    return json.dumps(0)



