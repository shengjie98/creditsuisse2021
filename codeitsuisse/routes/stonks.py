import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def stonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for test_case in data:
        energy = test_case.get("energy")
        capital = test_case.get("capital")
        timeline = test_case.get("timeline")
    return json.dumps(0)



