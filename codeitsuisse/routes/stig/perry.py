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
    logging.info("data sent for evaluation {}".format(interviews))
    # result = interpret_interviews(interviews)
    result = dumb(interviews)

    logging.info("My result :{}".format(result))
    return app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

def dumb(data):
    ans = []
    for test_case in data:
        p = 0
        for q in test_case['questions']:
            p += q[0]["to"] - q[0]["from"]

        q = test_case["maxRating"]
        hcf = gcd(p, q)

        ans.append({"p": p//hcf, "q": q//hcf})

    return ans


def interpret_interviews(interviews: list):
    interview_outputs = []
    for interview in interviews:
        max_rating = interview["maxRating"]
        questions = interview["questions"]

        D = initializeDiffArray()
        for question in questions:
            update(D, question[0]['from'], question[0]['to'])
        A = scanArray(D)
        print(A)
        # interview_outputs.append(output)
    return interview_outputs

def initializeDiffArray():
    

    # We use one extra space because
    # update(l, r, x) updates D[r+1]
    # D = [0 for i in range(0 , n + 1)]

    # D[0] = A[0]; D[n] = 0
    # for i in range(1, n ):
    #     D[i] = A[i] - A[i - 1]
    return defaultdict(int)

# Does range update
def update(D, l, r):
    D[l] += 1
    D[r + 1] -= 1

# Prints updated Array
def scanArray(D):
    A = defaultdict(int)
    print(D)
    for i, (key, val) in enumerate(sorted([(k, v) for k, v in D.items()])):
        if i == 0:
            A[i] = val
        else:
            A[i] = val + A[i-1]
    for i in range(0 , len(A)):
        if (i == 0):
            A[i] = D[i]
    return A
    #     # Note that A[0] or D[0] decides
    #     # values of rest of the elements.
    #     else:
    #         A[i] = D[i] + A[i - 1]

    #     print(A[i], end = " ")
        
    # print ("")