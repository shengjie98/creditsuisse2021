import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def get_id():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    # logging.info("My result :{}".format(result))
    return json.dumps(0)



