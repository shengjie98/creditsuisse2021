import logging
import json
from collections import defaultdict

from flask import request, jsonify
from itertools import product
from math import gcd

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route("/stig/perry", methods=["POST"])
def perry():
    interviews = request.get_json()
    # logging.info("data sent for evaluation {}".format(interviews))
    # result = interpret_interviews(interviews)
    result = []
    for test_case in interviews:
        result.append(dumb(test_case))

    logging.info("My result :{}".format(result))
    return app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

def dumb(test_case):
    arr = []
    for i, q in enumerate(test_case['questions']):
        arr.append((q[0]["from"], i, False))
        arr.append((q[0]["to"], i, True))
    arr.append((1, -1, False))
    arr.append((1e9, -1, True))
    arr.sort(key=lambda x: x[2])
    arr.sort(key=lambda x: x[0])
    logging.info("made arr")
    S = []
    ans = []
    for i in range(1, len(arr)):
        n, a, e = arr[i-1]
        m, _, f = arr[i]
        if e == False:
            S.append(a)
        else:
            S.remove(a)
        n_prime = n + 1 if e else n
        m_prime = m if f else m - 1
        if n_prime <= m_prime:
            ans.append(','.join(map(str, sorted(tuple(S)))))
    p = len(set(ans))
    logging.info("after getting ans")
    q = 1000000000
    factor = gcd(p, q)
    return {
        "p": int(p//factor),
        "q": int(q//factor)
    }



