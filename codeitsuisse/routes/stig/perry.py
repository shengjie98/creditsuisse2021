import logging
import json

from flask import request, jsonify
from itertools import product

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route("/stig/perry", methods=["POST"])
def perry():
    interviews = request.get_json()
    logging.info("data sent for evaluation {}".format(interviews))
    # result = interpret_interviews(interviews)

    # logging.info("My result :{}".format(result))
    return json.dumps(0)

def all_repeat(rno):
    results = []
    for c in product([True, False], repeat = rno):
        results.append(c)
    return results

def interpret_interviews(interviews: list):
    interview_outputs = []
    for interview in interviews:
        max_rating = interview["maxRating"]
        questions = interview["questions"]

        sets = []
        

        output = {p: 1, q: high - low + 1}
        interview_outputs.append(output)
    return interview_outputs

