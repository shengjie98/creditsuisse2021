import logging
import json
import requests
import sseclient

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

url = "https://cis2021-arena.herokuapp.com/quoridor/start/"
play_url = "https://cis2021-arena.herokuapp.com/quoridor/play/"

@app.route('/quoridor', methods=['POST'])
def get_quo():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data['battleId']
    endpoint = url + battleId
    play_end = play_url + battleId

    stream_response = requests.get(endpoint, stream=True)
    client = sseclient.SSEClient(stream_response)

    to_post = {
        "action": "(╯°□°)╯︵ ┻━┻"
    }
    x = requests.post(play_end, json = to_post)
    logging.info(x.status_code, to_post)
    return json.dumps(0)
    # Loop forever (while connection "open")
    # for i, event in enumerate(client.events()):
    #     logging.info(event.data)
    #     d = json.loads(event.data)
    #     if i == 0:
    #         # board = createBoard()   
    #         player = d['youAre']
    #         if player == 'second':
    