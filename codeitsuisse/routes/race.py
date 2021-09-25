import logging
import json

from flask import request, jsonify

from collections import Counter
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def race():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))
    with open('results.txt') as f:
        lines = f.readlines()
    all_racers = []
    for line in lines:
        racers = line.lstrip('Your guess is ').split(', ')
        racers[-1] = racers[-1].split('.')[0]
        all_racers.extend(racers)
    ctr = Counter(all_racers)
    swimmers = data.split(',')
    swimmers.sort(key=lambda x: ctr[x])     
    return ','.join(swimmers)



