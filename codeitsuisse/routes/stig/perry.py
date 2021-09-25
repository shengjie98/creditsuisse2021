import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route("/stig/perry", methods=["POST"])
def perry():
    interviews = request.get_json()
    logging.info("data sent for evaluation {}".format(interviews))
    result = interpret_interviews(interviews)

    logging.info("My result :{}".format(result))
    return json.dumps(result)


def interpret_interviews(interviews: list) -> list:
    interview_outputs = []
    for interview in interviews:
        max_rating = interview["maxRating"]
        questions = interview["questions"]

        low = 1
        high = max_rating

        for question in questions:
            interval = question[0]  # each question contains only one interval

            low = max(low, interval["from"])
            high = min(high, interval["to"])

        output = {p: 1, q: high - low + 1}
        interview_outputs.append(output)
    return interview_outputs

