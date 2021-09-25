import logging
import json

from flask import request, jsonify

from codeitsuisse import app


from hashlib import sha256

logger = logging.getLogger(__name__)

@app.route('/cipher-cracking', methods=['POST'])
def crack():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    for d in data:
        D = d['D']
        X = d["X"]
        Y = d["Y"]
        logging.info(Y)
        
    return json.dumps(0)

