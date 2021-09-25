import logging
import json
import requests
import sseclient

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

url = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/"

@app.route('/tic-tac-toe', methods=['POST'])
def get_id():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data['battleId']
    endpoint = url + battleId

    stream_response = requests.get(endpoint, stream=True)

    client = sseclient.SSEClient(stream_response)

    # Loop forever (while connection "open")
    for event in client.events():
        logging.info("got a new event from server")
        logging.info(event.data)
    
    
    # logging.info("My result :{}".format(result))
    return json.dumps(0)



