import logging
import json

from flask import request, jsonify
from itertools import combinations_with_replacement

from codeitsuisse import app

logger = logging.getLogger(__name__)

def clear_criteria(s, guess, result):
    wrong_pos = result // 10
    correct_pos = result % 10
    if correct_pos == sum([s[i] == guess[i] for i in range(len(s))]) and wrong_pos == sum([s[i] in guess and s[i] != guess[i] for i in range(len(s))]):
        return True
    else:
        return False

def get_possible_results(num_slots):
    ans = []
    for ten in range(num_slots+1):
        for ones in range(num_slots - ten + 1):
            if ten == 1 and ones == num_slots -1:
                pass
            else:
                ans.append(ten * 10 + 1)

@app.route('/decoder', methods=['POST'])
def decode():
    data = request.get_json()
    possible_values = data['possible_values']
    num_slots = data['num_slots']
    history = data['history']
    possible_results = get_possible_results(num_slots)
    
    possible = []
    for s in combinations_with_replacement(possible_values, num_slots):
        flag = True
        if not history:
            guess = [possible_values[0]] * (num_slots // 2) + [possible_values[1]] * (num_slots - num_slots // 2)
            json.dumps(guess)
        for h in history:
            guess = tuple(h['output_received'])
            result = h['result']
            if not clear_criteria(s, guess, result):
                flag = False
                break
        if flag:
            possible.append(s)

    best_guess = None
    max_score = 0
    for next_guess in possible:
        score = 0
        for res in possible_results:
            score = max(score, filter(lambda x: not clear_criteria(x, next_guess, res), possible))
        if score > max_score:
            max_score = score
            best_guess = next_guess
            
    return json.dumps(best_guess)
