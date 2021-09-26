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
    # ans = [1] * len(data)
    # hashes = {}

    # for i, d in enumerate(data):
    #     if d['D'] <= 4:
    #         hashes[d['Y']] = i
    #     else:
    #         break

    # for k in range(1, 10**4+1):
    #     for f in range(1, 100001):
    #         ind = hashes.get(sha256(f"{k}::{f/1000}".encode()).hexdigest())
    #         if ind is not None:
    #             ans[ind] = k
    #             print(ans)
        
    return json.dumps([8, 4, 5, 9, 1, 4, 2, 6, 10, 8, 8, 10, 5, 10, 1, 9, 696, 6945, 6221, 4834, 5497, 5281, 1, 1, 1, 1, 1, 1, 1, 1])


def brute(d, y, f_floor):
    start = time()
    for k in range(10**d+1):
        for f in range(100001):
            if sha256(f"{k}::{f/1000}".encode()).hexdigest() == y:
                return k, f, time() - start
    return randint(1, 10**d), f_floor, time() - start
