import logging
import json

from flask import request, jsonify

from collections import Counter, defaultdict
from codeitsuisse import app
import random

logger = logging.getLogger(__name__)


@app.route("/fixedrace", methods=["POST"])
def random_race():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))

    swimmers = data.split(",")
    random.shuffle(swimmers)

    return ",".join(swimmers)


def race_2():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))

    ranking = defaultdict(
        set
    )  # {"A" : ["B", "C", "D"]} if A won in a race with A,B,C,D

    # Use past results to build a ranking
    with open("results.txt") as f:
        lines = f.readlines()
        for line in lines:
            racers = line.lstrip("Your guess is ").split(", ")
            racers[-1] = racers[-1].split(".")[0]
            winner = line.split(".")[-3].lstrip(" Winner of this race is ")

            for racer in racers:
                if winner != racer:
                    ranking[racer] = winner

        logging.info(f"Racers: {racers}")
        logging.info(f"Winner: {winner}")

    # Use ranking to rank the input swimmers
    swimmers = data.split(",")
    seen = set()
    for swimmer in swimmers:
        # If there are any other swimmers who we know is faster, we add to stack. If no other swimmers, we append to output first from the stack. Then continue considering other swimmers.
        if swimmer in seen:
            continue
        stack = [swimmer]
        swimmers_set = set(swimmers)
        for better_swimmer in ranking[swimmer]:

            if summers_set.has(better_swimmer):
                stack.append(better_swimmer)

        if set(swimmers).intersection(ranking[swimmer]):
            pass
            # Find the swimmer to add to stack

    return ",".join(swimmers)


def race():
    data = request.get_data(as_text=True)
    logging.info("data sent for evaluation {}".format(data))
    with open("results.txt") as f:
        lines = f.readlines()
    all_racers = []
    for line in lines:
        racers = line.lstrip("Your guess is ").split(", ")
        racers[-1] = racers[-1].split(".")[0]
        all_racers.extend(racers)
    ctr = Counter(all_racers)
    for line in lines:
        winner = line.split(".")[-3].lstrip(" Winner of this race is ")
        racers = line.lstrip("Your guess is ").split(", ")
        max_racer = max([ctr[racer] for racer in racers])
        ctr[winner] = max_racer

    swimmers = data.split(",")
    swimmers.sort(key=lambda x: ctr[x], reverse=True)
    return ",".join(swimmers)

