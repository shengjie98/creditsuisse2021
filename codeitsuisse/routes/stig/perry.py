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
    result = dumb(interviews)

    logging.info("My result :{}".format(result))
    return app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

def dumb(data):
    res = []
    for test_case in data:
        logging.info(len(test_case['questions']))
        arr = []
        for i, q in enumerate(test_case['questions']):
            arr.append((q[0]["from"], i, False))
            arr.append((q[0]["to"], i, True))
        arr.append((1, -1, False))
        arr.append((1e9, -1, True))
        arr.sort(key=lambda x: x[2])
        arr.sort(key=lambda x: x[0])
        S = set()
        ans = []
        for i in range(1, len(arr)):
            n, a, e = arr[i-1]
            m, b, f = arr[i]
            if e == False:
                S.add(a)
            else:
                S.remove(a)
            n_prime = n + 1 if e else n
            m_prime = m if f else m - 1
            if n_prime <= m_prime:
                ans.append((n_prime, m_prime, S.copy()))
        all_possible_sets = {tuple(sorted(tuple(n[2]))) for n in ans}
        print(all_possible_sets)
        p = len(all_possible_sets)
        q = 1e9
        factor = gcd(p, q)
        res.append({
            "p": int(p//factor),
            "q": int(q//factor)
        })
    return res

def gcd(a,b):
    if a == 0:
        return b
    return gcd(b % a, a)
 
# Function to return LCM of two numbers
def lcm(a,b):
    return (a / gcd(a,b))* b



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