import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = [ast(i) for i in data.get('test_cases')]
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
    cleanstr.append(seq[len(seq)-1])
    dp = [[-1]*len(cleanlens) for i in range(len(cleanlens))]
    pos = [[-1]*len(cleanlens) for i in range(len(cleanlens))]
    prop = [[False]*len(cleanlens) for i in range(len(cleanlens))]

    res = longest_palindrome(cleanstr, 0, len(cleanlens)-1, dp, cleanlens, pos, prop)
    # print(dp)
    # print(pos)
    # print(''.join(cleanstr))
    # print(sum(cleanlens))
    # print(res)

    origin = sum(cleanlens[:res[1]]) + cleanlens[res[1]] // 2

    res = {
        "input": seq,
        "score": int(res[0]) if int(res[0]) == res[0] else res[0],
        "origin": origin
    }

    return res

def multiplier(length: int):
    if length >= 10:
        return 2 * length
    
    return 1.5 * length if length >= 7 else length

def longest_palindrome(cleanstr: list, start: int, end: int, dp: list, cleanlens: list, pos: list, prop: list):
    if start == end:
        prop[start][end] = True
        if cleanlens[start] == 2:
            prop[start][end] = False
        elif cleanlens[start] == 1:
            if start == 0 or end == len(cleanlens) - 1 or (cleanstr[start-1] != cleanstr[end+1]):
                prop[start][end] = False
        if prop[start][end]:
            dp[start][end] = multiplier(cleanlens[start])
        else:
            dp[start][end] = 1
        pos[start][end] = start
        return dp[start][end], pos[start][end], prop[start][end]
    
    if dp[start][end] > 0:
        return dp[start][end], pos[start][end], prop[start][end]

    else:
        if cleanstr[start] != cleanstr[end]:
            take_start = longest_palindrome(cleanstr, start, end-1, dp, cleanlens, pos, prop)
            take_end = longest_palindrome(cleanstr, start+1, end, dp, cleanlens, pos, prop)

            # if start == 0 and end == len(cleanstr)-1:
            #     _start = longest_palindrome(cleanstr, start, start, dp, cleanlens, pos)
            #     _end = longest_palindrome(cleanstr, end, end, dp, cleanlens, pos)
            #     take_start = take_start[0] + _end[0], take_start[1]
            #     take_end = take_end[0] + _start[0], take_end[1]

            # print(f"{start}, {end}: takestart: {take_start}, takeend:{take_end}")

            if take_start[0] > take_end[0]:
                dp[start][end] = take_start[0]
                pos[start][end] = take_start[1]
                prop[start][end] = take_start[2]
            else:
                dp[start][end] = take_end[0]
                pos[start][end] = take_end[1]
                prop[start][end] = take_end[2]

        else:
            sub = longest_palindrome(cleanstr, start+1, end-1, dp, cleanlens, pos, prop)
            # print(f"{start}, {end}: {sub}")
            if sub[2]:
                dp[start][end] = sub[0] + multiplier(cleanlens[start] + cleanlens[end])
            else:
                dp[start][end] = sub[0]
            pos[start][end] = sub[1]
            prop[start][end] = sub[2]

        return dp[start][end], pos[start][end], prop[start][end]
