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
    fs = []
    ds = []
    currd = 1
    for i in range(len(data)):
        d = data[i]
        if d['D'] == currd:
            ds.append((d['X'], i))
        else:
            fs.append(sorted(ds))
            ds = []

    ans = [1] * len(data)

    for D, ds in enumerate(fs):
        if D > 2:
            continue
        
        f_floor = 0
        for d in ds:
            k, f_floor, t = brute(D+1, data[d[1]]['Y'], f_floor)
            ans[d[1]] = k


    # for d in data[::-1]:
    #     D = d['D']
    #     # X = d["X"]
    #     Y = d["Y"]
    #     if D <= 3 and time_taken <= 28:
    #         k, t, f_floor = brute(D, Y, f_floor)
    #         ans.append(k)
    #         time_taken += t
    #     else:
    #         ans.append(1)

        # logging.info(Y)
        
    return json.dumps(ans[::-1])


def brute(d, y, f_floor):
    start = time()
    for k in range(10**d):
        for f in range(100000):
            if sha256(f"{k}::{f/1000}".encode()).hexdigest() == y:
                return k, f, time() - start
    return randint(1, 10**d), f_floor, time() - start
