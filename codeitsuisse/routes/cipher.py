import logging
import json
from hashlib import sha256
from time import time
from random import randint

from flask import request, jsonify

from codeitsuisse import app


from hashlib import sha256

logger = logging.getLogger(__name__)

@app.route('/cipher-cracking', methods=['POST'])
def crack():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    time_taken = 0
    for d in data:
        D = d['D']
        # X = d["X"]
        Y = d["Y"]
        if D <= 4 and time_taken <= 28:
            k, t = brute(D, Y)
            ans.append(k)
            time_taken += t
        else:
            ans.append(1)

        logging.info(Y)
        
    return json.dumps(ans)


def brute(d, y):
    start = time()
    for k in range(10**d):
        for f in range(100000):
            if sha256(f"{k}::{f/1000}".encode()).hexdigest() == y:
                return k, time() - start
    return randint(1, 10**d), time() - start
