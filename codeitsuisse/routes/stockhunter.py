import logging
import json
import math
from heapq import heappush, heappop

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

from collections import defaultdict
import heapq


@app.route("/stock-hunter", methods=["POST"])
def stock_hunter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    outputs = []
    for testcase in data:
        output = handle_testcase(testcase)
        outputs.append(output)

    logging.info("My results :{}".format(outputs))
    return json.dumps(outputs)


def handle_testcase(testcase):
    start = (testcase["entryPoint"]["first"], testcase["entryPoint"]["second"])
    end = (testcase["targetPoint"]["first"], testcase["targetPoint"]["second"])
    grid_depth = testcase["gridDepth"]
    grid_key = testcase["gridKey"]
    h_step = testcase["horizontalStepper"]
    v_step = testcase["verticalStepper"]

    ROWS = end[0] - start[0] + 1
    COLS = end[1] - start[1] + 1

    # We can find the worst case where we need to extend the matrix to the right and to the bottom. --> extra cols = ROWS, probably extra rows - COLS
    risk_index_matrix = [[-1] * (COLS + ROWS) for _ in range(ROWS + COLS)]
    risk_level_matrix = [[-1] * (COLS + ROWS) for _ in range(ROWS + COLS)]

    # Calculate risk index of every cell up till target cell, since depends on left and upper cell.

    risk_index_matrix[start[0]][start[1]] = 0
    risk_index_matrix[start[0]][start[1]] = 0

    risk_level_matrix[start[0]][start[1]] = (0 + grid_depth) % grid_key
    risk_level_matrix[end[0]][end[1]] = (0 + grid_depth) % grid_key

    # Calc risk of top level
    for c in range(1, ROWS + COLS):
        risk_index_matrix[0][c] = c * h_step
        risk_level_matrix[0][c] = (c * h_step + grid_depth) % grid_key

    # Calc risk of left level
    for r in range(1, ROWS + COLS):
        risk_index_matrix[r][0] = r * v_step
        risk_level_matrix[r][0] = (r * v_step + grid_depth) % grid_key

    # Calc risk of every other cell
    for r in range(1, ROWS + COLS):
        for c in range(1, ROWS + COLS):
            risk_index = risk_level_matrix[r - 1][c] * risk_level_matrix[r][c - 1]
            risk_index_matrix[r][c] = risk_index
            risk_level_matrix[r][c] = (risk_index + grid_depth) % grid_key

    grid_map = []
    for r in range(ROWS + COLS):
        this_row = []
        for c in range(ROWS + COLS):
            risk_level = risk_level_matrix[r][c]

            if risk_level % 3 == 0:
                risk_cost = "L"
            elif risk_level % 3 == 1:
                risk_cost = "M"
            else:
                risk_cost = "S"
            this_row.append(risk_cost)

        grid_map.append(this_row)

    min_cost = find_minimum_cost(grid_map, start, end)

    return {"gridMap": grid_map, "minimumCost": min_cost}


def find_minimum_cost(grid_map: list, source: tuple, target: tuple):
    ROWS = len(grid_map)
    COLS = len(grid_map[0])

    def get_val(coords):
        risk_cost = grid_map[coords[0]][coords[1]]
        if risk_cost == "L":
            return 3
        elif risk_cost == "M":
            return 2
        elif risk_cost == "S":
            return 1
        return 0

    minheap = []
    cost = 0
    seen = set()
    dist = {}

    heapq.heappush(minheap, (get_val(source), source))
    seen.add(source)

    while minheap:
        # pop from minheap
        new_cost, coord = heapq.heappop(minheap)
        cost += new_cost
        logging.info(f"Coord: {coord[0]},{coord[1]} - cost: {cost}")

        if coord == target:
            return cost

        # set this coord as seen
        seen.add(coord)

        # for neighbours, if not already seen, add to heap
        r, c = coord
        positions = [
            (r + 1, c),
            (r - 1, c),
            (r, c + 1),
            (r, c - 1),
        ]
        for nr, nc in positions:
            if nr == -1 or nr == ROWS or nc == -1 or nc == COLS:
                continue
            if (nr, nc) in seen:
                continue

            alt_cost = cost + get_val((nr, nc))
            if (nr, nc) not in dist:
                dist[(nr, nc)] = alt_cost
            else:
                if dist[(nr, nc)] > alt_cost:
                    dist[(nr, nc)] = alt_cost

            heapq.heappush(minheap, (get_val((nr, nc)), (nr, nc)))

    return cost


# def evaluateStockhunter():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     results = []
#     keys = 'LMS'
#     convert = lambda x: keys[3-x]
#     for d in data:
#         grid, start, end = make_grid(d)
#         dist, row_lim, col_lim = dikstraw(grid, start, end)

#         grid = [list(map(convert, row[:col_lim+1])) for row in grid[:row_lim + 1]]

#         results.append(
#             {
#                 'gridMap': grid,
#                 'minimumCost': dist
#             }
#         )


#     logging.info("My results :{}".format(results))
#     return json.dumps(results)

# def make_grid(data: dict):
#     start = data['entryPoint']['first'], data['entryPoint']['second']
#     end = data['targetPoint']['first'], data['targetPoint']['second']

#     depth = data['gridDepth']
#     key = data['gridKey']
#     h_stepper = data['horizontalStepper']
#     v_stepper = data['verticalStepper']

#     corner = math.ceil((end[1]+1)*1.5), math.ceil((end[0]+1)*1.5)
#     print(corner)

#     grid = [[0]*corner[0] for i in range(corner[1])]

#     for row in range(corner[1]):
#         for col in range(corner[0]):
#             if (col, row) == start:
#                 index = 0
#             elif row == 0:
#                 index = h_stepper * col
#             elif col == 0:
#                 index = v_stepper * row
#             else:
#                 index = grid[row][col-1] * grid[row-1][col]

#             grid[row][col] = (index + depth) % key

#     for row in range(corner[1]):
#         for col in range(corner[0]):
#             grid[row][col] = 3 - grid[row][col] % 3

#     # print(grid)

#     return grid, start, end


# DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# def get_neighbours(grid: list, curr: tuple): # curr is (col, row)
#     bounds = len(grid[0]), len(grid)
#     neighbours = []

#     for d in DIRECTIONS:
#         neighbour = curr[0] + d[0], curr[1] + d[1]
#         if 0 <= neighbour[0] < bounds[0] and 0<= neighbour[1] < bounds[1]:
#             neighbours.append(neighbour)

#     return neighbours


# def dikstraw(grid: list, start: tuple, end: tuple):
#     parents = [[-1] * len(grid) for _ in range(len(grid[0]))]
#     dists = [[-1] * len(grid) for _ in range(len(grid[0]))]
#     dist = 0#grid[start[1]][start[0]]

#     pq = []
#     dists[start[1]][start[0]] = dist

#     heappush(pq, (dist, start))

#     while len(pq):
#         dist, curr = heappop(pq)
#         if dist > dists[curr[1]][curr[0]]:
#             continue
#         if curr == end:
#             break

#         for n in get_neighbours(grid, curr):
#             if dists[n[1]][n[0]] < 0 or (dists[n[1]][n[0]] > 0 and dist + grid[n[1]][n[0]] < dists[n[1]][n[0]]):
#                 dists[n[1]][n[0]] = dist + grid[n[1]][n[0]]
#                 parents[n[1]][n[0]] = curr
#                 heappush(pq, (dists[n[1]][n[0]], n))

#     col_lim, row_lim = curr

#     while parents[curr[1]][curr[0]] != -1:
#         curr = parents[curr[1]][curr[0]]
#         col_lim = curr[0] if curr[0] > col_lim else col_lim
#         row_lim = curr[1] if curr[1] > row_lim else row_lim

#     print(dists)
#     return dist, row_lim, col_lim

