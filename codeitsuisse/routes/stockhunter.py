import logging
import json
import math
from heapq import heappush, heappop

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluateStockhunter():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    keys = 'LMS'
    convert = lambda x: keys[3-x]
    for d in data:
        grid, start, end = make_grid(d)
        dist, row_lim, col_lim, path = dikstraw(grid, start, end)

        print(path)
        for r in grid:
            print(r)

        grid = [list(map(convert, row[:col_lim+1])) for row in grid[:row_lim + 1]]


        results.append(
            {
                'gridMap': grid,
                'minimumCost': dist
            }
        )


    logging.info("My results :{}".format(results))
    return json.dumps(results)

def make_grid(data: dict):
    start = data['entryPoint']['first'], data['entryPoint']['second']
    end = data['targetPoint']['first'], data['targetPoint']['second']

    depth = data['gridDepth']
    key = data['gridKey']
    h_stepper = data['horizontalStepper']
    v_stepper = data['verticalStepper']

    corner = math.ceil((end[0]+1)*2), math.ceil((end[1]+1)*2)
    print(corner)

    grid = [[0]*corner[0] for i in range(corner[1])]

    for row in range(corner[1]):
        for col in range(corner[0]):
            if (col, row) == start:
                index = 0
            elif row == 0:
                index = h_stepper * col
            elif col == 0:
                index = v_stepper * row
            else:
                index = grid[row][col-1] * grid[row-1][col]
            
            grid[row][col] = (index + depth) % key

    for row in range(corner[1]):
        for col in range(corner[0]):
            grid[row][col] = 3 - grid[row][col] % 3

    # print(grid)

    return grid, start, end


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
def get_neighbours(grid: list, curr: tuple): # curr is (col, row)
    bounds = len(grid[0]), len(grid)
    neighbours = []

    for d in DIRECTIONS:
        neighbour = curr[0] + d[0], curr[1] + d[1]
        if 0 <= neighbour[0] < bounds[0] and 0<= neighbour[1] < bounds[1]:
            neighbours.append(neighbour)

    return neighbours


def dikstraw(grid: list, start: tuple, end: tuple):
    parents = [[-1] * len(grid[0]) for _ in range(len(grid))]
    dists = [[-1] * len(grid[0]) for _ in range(len(grid))]
    dist = 0#grid[start[1]][start[0]]

    pq = []
    dists[start[1]][start[0]] = dist

    heappush(pq, (dist, start))

    while len(pq):
        dist, curr = heappop(pq)
        if dist > dists[curr[1]][curr[0]] :
            continue
        if curr == end:
            break

        for n in get_neighbours(grid, curr):
            if dists[n[1]][n[0]] < 0 or (dists[n[1]][n[0]] >= 0 and dist + grid[n[1]][n[0]] < dists[n[1]][n[0]]):
                dists[n[1]][n[0]] = dist + grid[n[1]][n[0]]
                parents[n[1]][n[0]] = curr
                heappush(pq, (dists[n[1]][n[0]], n))

    col_lim, row_lim = curr
    path = [curr]

    while parents[curr[1]][curr[0]] != -1:
        curr = parents[curr[1]][curr[0]]
        path.append(curr)
        col_lim = curr[0] if curr[0] > col_lim else col_lim
        row_lim = curr[1] if curr[1] > row_lim else row_lim

    # print(dists)
    return dists[end[1]][end[0]], row_lim, col_lim, path
