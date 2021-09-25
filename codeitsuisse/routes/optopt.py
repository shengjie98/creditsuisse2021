import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/optopt', methods=['POST'])
def optopt():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    return json.dumps(0)

def helplah(options, views):
    expected_market_val = 0
    total_weight = 0
    for v in views:
        expected_market_val += v['mean'] * v['weight']
        total_weight += v['weight']

    expected_market_val /= total_weight

    for o in options:
        continue
        if o['type'] == 'call':
            pass
        # o['expectation'] = 

