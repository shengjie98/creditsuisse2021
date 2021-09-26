import logging
import json
from random import random, randrange

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/optopt', methods=['POST'])
def optopt():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    rng = helplah(**data)
    logging.info(f"rngsus has blessed :{rng}")

    return json.dumps(rng)

def helplah(options, view):
    expected_market_val = 0
    total_weight = 0
    for v in view:
        expected_market_val += v['mean'] * v['weight']
        total_weight += v['weight']

    expected_market_val /= total_weight

    for o in options:
        if o['type'] == 'call':
            o['expectation'] = max(o['premium'], expected_market_val - o['strike'] - o['premium'])
        else:
            o['expectation'] = max(o['strike'] - o['premium'] - expected_market_val, o['premium'])

    best = 0
    for i in range(len(options)):
        if options[i]['expectation'] > options[best]['expectation']:
            best = i

    shares = [0] * len(options)
    shares[best] = randrange(-100, 100)

    return shares


# def rngsus(options, view):
#     rng = [random() for i in range(len(options))]
#     total = sum(rng)
#     for i in range(len(rng)):
#         rng[i] = int(100 * rng[i]/total)
    
#     total = sum(rng)
#     while total > 100:
#         randind = randrange(0, len(options))
#         rng[randind] -= 1
#         total -= 1
    
#     for i in range(len(rng)):
#         if options[i]['type'] == 'put':
#             rng[i] *= -1

#     return rng
    

    