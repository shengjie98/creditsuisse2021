import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route("/asteroid", methods=["POST"])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = [ast(i) for i in data.get("test_cases")]
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def ast(s: str):
    """
        >= 10 --> x2
        7-9 --> x1.5
        <= 6 --> x1
    """
    # Tries every possible index as origin and take the maximum score
    def get_score(origin, s):
        # For a given origin index, find the score
        # E.g. "AABBBCCCCBBBA"
        if not 0 <= origin < len(s):
            return 0

        score = 0
        l = origin
        r = origin
        count = 1

        # Will explosion propogate
        while True:
            if l == origin and r == origin:
                if not (l - 1 >= 0 and r + 1 < len(s) and s[l - 1] == s[r + 1]):
                    break  # no propogate
            else:
                if not (l >= 0 and r < len(s) and s[l] == s[r]):
                    break  # no propogate

            current_char = s[l]
            # logging.info(f"Current char: {current_char}")

            # logging.info(count)

            # Exhaust left side
            while l - 1 >= 0 and s[l - 1] == current_char:
                l -= 1
                count += 1
            # logging.info(count)

            # Exhuast right side
            while r + 1 < len(s) and s[r + 1] == current_char:
                r += 1
                count += 1
            # logging.info(count)

            # Use count to calculate score
            if count >= 10:
                score += count * 2
            elif count >= 7:
                score += count * 1.5
            else:
                score += count

            # Shift pointers for next explosion
            l -= 1
            r += 1
            count = 2

        return score

    max_score = 0
    for i in range(len(s)):
        new_score = get_score(i, s)
        logger.info(f"Origin: {i} Score: {new_score}")
        max_score = max(max_score, new_score)

    return max_score


def ast_bad(s: str):
    # Greedily get longest substr with consecutive chars (the start and end index) of s
    # array to store how many same characters are there on its left and right.
    left_consec = [0]
    right_consec = [0]

    most_frequent_left_index = 0
    largest_frequency = 0

    current_char = s[0]
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            new_frequency = left_consec[i - 1] + 1
            if new_frequency > largest_frequency:
                largest_frequency = new_frequency
                most_frequent_left_index = i
            left_consec.append(left_consec[i - 1] + 1)
        else:
            current_char = s[i]
            left_consec.append(0)

    most_frequent_right_index = 0
    largest_frequency = 0

    current_char = s[-1]
    for i in range(len(s) - 2, -1, -1):
        if s[i] == s[i + 1]:
            new_frequency = right_consec[i + 1] + 1
            if new_frequency > largest_frequency:
                largest_frequency = new_frequency
                most_frequent_right_index = i
            right_consec.append(right_consec[i + 1] + 1)
        else:
            current_char = s[i]
            right_consec.append(0)
    right_consec.reverse()

    logging.info(f"Largest left index: {most_frequent_left_index}")
    logging.info(f"Largest right index: {most_frequent_right_index}")


def ast_old(seq: str):
    cleanstr = []
    cleanlens = []

    length = 1
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:
            cleanlens.append(length)
            cleanstr.append(seq[i - 1])
            length = 1
        else:
            length += 1

    cleanlens.append(length)
    cleanstr.append(seq[len(seq) - 1])
    dp = [[-1] * len(cleanlens) for i in range(len(cleanlens))]
    pos = [[-1] * len(cleanlens) for i in range(len(cleanlens))]
    prop = [[False] * len(cleanlens) for i in range(len(cleanlens))]

    res = longest_palindrome(cleanstr, 0, len(cleanlens) - 1, dp, cleanlens, pos, prop)
    # print(dp)
    # print(pos)
    # print(''.join(cleanstr))
    # print(sum(cleanlens))
    # print(res)

    origin = (
        sum(cleanlens[: res[1]]) + cleanlens[res[1]] // 2 - (cleanlens[res[1]] % 2 == 0)
    )

    res = {"input": seq, "score": res[0], "origin": origin}

    return res


def multiplier(length: int):
    if length >= 10:
        return 2 * length

    return 1.5 * length if length >= 7 else length


def longest_palindrome(
    cleanstr: list,
    start: int,
    end: int,
    dp: list,
    cleanlens: list,
    pos: list,
    prop: list,
):
    if start == end:
        prop[start][end] = cleanlens[start] > 2
        if prop:
            dp[start][end] = multiplier(cleanlens[start])
        else:
            dp[start][end] = 0
        pos[start][end] = start
        return dp[start][end], pos[start][end], prop

    if dp[start][end] > 0:
        return dp[start][end], pos[start][end], prop[start][end]

    else:
        if cleanstr[start] != cleanstr[end]:
            take_start = longest_palindrome(
                cleanstr, start, end - 1, dp, cleanlens, pos, prop
            )
            take_end = longest_palindrome(
                cleanstr, start + 1, end, dp, cleanlens, pos, prop
            )

            # if start == 0 and end == len(cleanstr)-1:
            #     _start = longest_palindrome(cleanstr, start, start, dp, cleanlens, pos)
            #     _end = longest_palindrome(cleanstr, end, end, dp, cleanlens, pos)
            #     take_start = take_start[0] + _end[0], take_start[1]
            #     take_end = take_end[0] + _start[0], take_end[1]

            # print(f"{start}, {end}: takestart: {take_start}, takeend:{take_end}")

            if take_start[0] > take_end[0]:
                dp[start][end] = take_start[0]
                pos[start][end] = take_start[1]
            else:
                dp[start][end] = take_end[0]
                pos[start][end] = take_end[1]

        else:
            sub = longest_palindrome(
                cleanstr, start + 1, end - 1, dp, cleanlens, pos, prop
            )
            # print(f"{start}, {end}: {sub}")
            if sub[2]:
                dp[start][end] = sub[0] + multiplier(cleanlens[start] + cleanlens[end])
            else:
                dp[start][end] = sub[0]
            pos[start][end] = sub[1]
            prop[start][end] = sub[2]

        return dp[start][end], pos[start][end], prop[start][end]
