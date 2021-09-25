import logging
import json

from flask import request, jsonify
from itertools import product

from codeitsuisse import app

logger = logging.getLogger(__name__)


def clear_criteria(s, guess, result):
    return check(s, guess) == result

def check(ans, guess):
    if guess == ans:
        return 4

    a = list(ans[:])
    g = list(guess[:])
    correct = []
    wrong = 0
    for i in range(len(a)):
        if a[i] == g[i]:
            correct.append(i)
    for i in correct[::-1]:
        a.pop(i)
        g.pop(i)
    i = 0
    wrong = 0
    while i < len(a):
        if g[i] in a:
            a.remove(g[i])
            g.pop(i)
            wrong += 1
        else:
            i += 1
        
    right = len(correct)
    return wrong * 10 + right


def get_possible_results(num_slots):
    ans = []
    for ten in range(num_slots+1):
        for ones in range(num_slots - ten + 1):
            if ten == 1 and ones == num_slots -1:
                pass
            else:
                ans.append(ten * 10 + 1)
    return ans

def all_repeat(str1, rno):
    chars = list(str1)
    results = []
    for c in product(chars, repeat = rno):
        results.append(c)
    return results

@app.route('/decoder', methods=['POST'])
def decode():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    possible_values = data['possible_values']
    num_slots = data['num_slots']
    history = data['history']
    possible_results = get_possible_results(num_slots)
    
    if not history:
        guess = [possible_values[0]] * (num_slots // 2) + [possible_values[1]] * (num_slots - num_slots // 2)
        return json.dumps(guess)
    else:
        possible = []
        for s in all_repeat(possible_values, num_slots):
            flag = True
            for h in history:
                guess = tuple(h['output_received'])
                result = h['result']
                if not clear_criteria(s, guess, result):
                    flag = False
                    break
            if flag:
                possible.append(s)
        best_guess = possible[0]
        max_score = 0
        for next_guess in possible:
            score = 0
            for res in possible_results:
                score = max(score, len(list(filter(lambda x: not clear_criteria(x, next_guess, res), possible))))
            if score > max_score:
                max_score = score
                best_guess = next_guess

        json.dumps(best_guess)