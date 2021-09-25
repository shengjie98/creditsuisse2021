import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = [ast(i) for i in data]
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def ast(seq: str):
    cleanstr = []
    cleanlens = []

    length = 1
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]:
            cleanlens.append(length)
            cleanstr.append(seq[i-1])
            length = 1
        else:
            length += 1

    cleanlens.append(length)
    cleanstr.append(seq[i])
    dp = [[-1]*len(cleanlens) for i in range(len(cleanlens))]
    pos = [[-1]*len(cleanlens) for i in range(len(cleanlens))]

    res = longest_palindrome(cleanstr, 0, len(cleanlens)-1, dp, cleanlens, pos)

    origin = sum(cleanlens[:res[1]]) + cleanlens[res[1]] // 2

    res = {
        "input": seq,
        "score": int(res[0]),
        "origin": origin
    }
    return res

def multiplier(length: int):
    if length >= 10:
        return 2 * length
    
    return 1.5 * length if length > 7 else length

def longest_palindrome(cleanstr: list, start: int, end: int, dp: list, cleanlens: list, pos: list):
    if start == end:
        dp[start][end] = multiplier(cleanlens[start])
        pos[start][end] = start
        return dp[start][end], pos[start][end]
    
    if dp[start][end] > 0:
        return dp[start][end], pos[start][end]

    else:
        if cleanstr[start] != cleanstr[end]:
            take_start = longest_palindrome(cleanstr, start, end-1, dp, cleanlens, pos)
            take_end = longest_palindrome(cleanstr, start+1, end, dp, cleanlens, pos)

            if start == 0 and end == len(cleanstr)-1:
                _start = longest_palindrome(cleanstr, start, start, dp, cleanlens, pos)
                _end = longest_palindrome(cleanstr, end, end, dp, cleanlens, pos)
                take_start = take_start[0] + _end[0], take_start[1]
                take_end = take_end[0] + _start[0], take_end[1]

            if take_start[0] > take_end[0]:
                dp[start][end] = take_start[0]
                pos[start][end] = take_start[1]
            else:
                dp[start][end] = take_end[0]
                pos[start][end] = take_end[1]

        else:
            sub = longest_palindrome(cleanstr, start+1, end-1, dp, cleanlens, pos)
            dp[start][end] = sub[0] + multiplier(cleanlens[start] + cleanlens[end])
            pos[start][end] = sub[1]

        return dp[start][end], pos[start][end]
