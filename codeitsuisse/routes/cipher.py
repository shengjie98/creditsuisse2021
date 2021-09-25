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
    ans = [1] * len(data)
    hashes = {}

    for i, d in enumerate(data):
        if d['D'] < 4:
            hashes[d['Y']] = i
        else:
            break

    for k in range(1, 10**3):
        for f in range(1, 100000):
            ind = hashes.get(sha256(f"{k}::{f/1000}".encode()).hexdigest())
            if ind is not None:
                ans[ind] = k
        
    return json.dumps(ans[::-1])


def brute(d, y, f_floor):
    start = time()
    for k in range(10**d):
        for f in range(100000):
            if sha256(f"{k}::{f/1000}".encode()).hexdigest() == y:
                return k, f, time() - start
    return randint(1, 10**d), f_floor, time() - start
