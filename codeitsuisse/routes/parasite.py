import logging
import json
from flask import request, jsonify

from codeitsuisse import app

from copy import deepcopy

logger = logging.getLogger(__name__)


@app.route('/parasite', methods=['POST'])
def parasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data
    logging.info("Input", inputValue)

    ret = []

    for room in inputValue:

        room_number = room["room"]
        grid = room["grid"]
        interestedIndividuals = room["interestedIndividuals"]

        output = {}
        output["room"] = room_number
        output["p1"] = handleOne(grid, interestedIndividuals)
        output["p2"] = handleTwo(grid)
        output["p3"] = handleThree(grid)
        output["p4"] = handleFour(grid)

        ret.append(output)


    return json.dumps({"output": ret})

def handleOne(grid, interestedIndividuals):
    ''' Takes in grid of individuals and a list of interestedIndividuals, and outputs their final infection status  
    Parasite A can travel both horizontally and vertically. Calculate the time taken to infect a healthy person. Return -1 if person remains healthy or if the person is infected to begin with.
    '''

    '''
    "grid": [
      [0, 3, 2],
      [0, 1, 1],
      [1, 0, 0]
    ],
    "interestedIndividuals": [
      "0,2", "2,0", "1,2"
    ]


    "p1": { "0,2":  -1, "2,0":  -1, "1,2":  2},

    '''
    grid = deepcopy(grid)
    ret = {}

    # Check for coords of initial infected person
    initial_infected = (-1,-1)
    ROWS, COLS = len(grid), len(grid[0])
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 3:
                initial_infected = (r, c)
                break
        if initial_infected[0] != -1:
            break
    
    # Simulate infection
    
    seen = {}
    def infect_dfs(r, c, tick):
        # logging.info(f"r: {r}, c: {c}, tick: {tick}")

        if r == -1 or r == ROWS or c == -1 or c == COLS:
            # logging.info("Return due to OOB")
            return
        if (r,c) in seen:
            # logging.info("Return due to in seen")
            return
        if grid[r][c] == 2 or grid[r][c] == 0:
            seen[(r,c)] = -1
            # logging.info("Return due to not healthy")
            return


        grid[r][c] = 3
        seen[(r,c)] = tick
        # logging.info("Infected a new person!")
        

        infect_dfs(r+1, c, tick+1)
        infect_dfs(r-1, c, tick+1)
        infect_dfs(r, c+1, tick+1)
        infect_dfs(r, c-1, tick+1)

    infect_dfs(*initial_infected, 0) 

    for ind in interestedIndividuals:
        # Check if ind is already initially infected
        ind_pos = tuple(map(int, ind.split(",")))
        if ind_pos in seen:
            ret[ind] = seen[(ind_pos[0], ind_pos[1])]
        else:
            ret[ind] = -1

    return ret

def handleTwo(grid):
    ''' Returns how many ticks needed to infect whole room with horizontal and vertical spreading. '''
    grid = deepcopy(grid)
    ret = {}

    # Check for coords of initial infected person
    initial_infected = (-1,-1)
    ROWS, COLS = len(grid), len(grid[0])
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 3:
                initial_infected = (r, c)
                break
        if initial_infected[0] != -1:
            break
    
    # Simulate infection    
    seen = {}
    def infect_dfs(r, c, tick):
        # logging.info(f"r: {r}, c: {c}, tick: {tick}")

        if r == -1 or r == ROWS or c == -1 or c == COLS:
            # logging.info("Return due to OOB")
            return
        if (r,c) in seen:
            # logging.info("Return due to in seen")
            return
        if grid[r][c] == 2 or grid[r][c] == 0:
            seen[(r,c)] = -1
            # logging.info("Return due to not healthy")
            return


        grid[r][c] = 3
        seen[(r,c)] = tick
        # logging.info("Infected a new person!")
        

        infect_dfs(r+1, c, tick+1)
        infect_dfs(r-1, c, tick+1)
        infect_dfs(r, c+1, tick+1)
        infect_dfs(r, c-1, tick+1)

    infect_dfs(*initial_infected, 0) 

    max_tick = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1:
                return -1
            elif grid[r][c] == 3:
                max_tick = max(max_tick, seen.get((r,c), -1))

    return max_tick

def handleThree(grid):
    ''' Returns how many ticks needed to infect whole room with horizontal, vertical and diagonal spreading. '''
    grid = deepcopy(grid)
    ret = {}

    # Check for coords of initial infected person
    initial_infected = (-1,-1)
    ROWS, COLS = len(grid), len(grid[0])
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 3:
                initial_infected = (r, c)
                break
        if initial_infected[0] != -1:
            break
    
    # Simulate infection
    
    seen = {}
    def infect_dfs(r, c, tick):
        # logging.info(f"r: {r}, c: {c}, tick: {tick}")

        if r == -1 or r == ROWS or c == -1 or c == COLS:
            # logging.info("Return due to OOB")
            return
        if (r,c) in seen:
            # logging.info("Return due to in seen")
            return
        if grid[r][c] == 2 or grid[r][c] == 0:
            seen[(r,c)] = -1
            # logging.info("Return due to not healthy")
            return


        grid[r][c] = 3
        seen[(r,c)] = tick
        # logging.info("Infected a new person!")
        

        infect_dfs(r+1, c, tick+1)
        infect_dfs(r-1, c, tick+1)
        infect_dfs(r, c+1, tick+1)
        infect_dfs(r, c-1, tick+1)

        infect_dfs(r+1, c+1, tick+1)
        infect_dfs(r+1, c-1, tick+1)
        infect_dfs(r-1, c+1, tick+1)
        infect_dfs(r-1, c-1, tick+1)


    infect_dfs(*initial_infected, 0) 

    max_tick = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1:
                return -1
            elif grid[r][c] == 3:
                max_tick = max(max_tick, seen.get((r,c), -1))

    return max_tick

def handleFour(grid):
    ''' Returns amount of energy needed to infect whole room with horizontal, vertical and vacant space spreading. '''

    grid = deepcopy(grid)
    ret = {}

    # Check for coords of initial infected person
    initial_infected = (-1,-1)
    ROWS, COLS = len(grid), len(grid[0])
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 3:
                initial_infected = (r, c)
                break
        if initial_infected[0] != -1:
            break
    
    # Simulate infection
    
    seen = {}
    def infect_dfs_vacant(r, c, energy):
        # logging.info(f"r: {r}, c: {c}, energy: {energy}")

        if r == -1 or r == ROWS or c == -1 or c == COLS:
            # logging.info("Return due to OOB")
            return
        if (r,c) in seen:
            # logging.info("Return due to in seen")
            # Replace with lower energy if possible
            seen[(r,c)] = min(seen.get(r,c), energy)
            return
        if grid[r][c] == 2 or grid[r][c] == 0:
            # logging.info(f"adding energy at: {r},{c}")
            energy += 1
            seen[(r,c)] = energy   

        else:
            grid[r][c] = 3
            seen[(r,c)] = energy        

        infect_dfs_vacant(r+1, c, energy)
        infect_dfs_vacant(r-1, c, energy)
        infect_dfs_vacant(r, c+1, energy)
        infect_dfs_vacant(r, c-1, energy)


    infect_dfs_vacant(*initial_infected, 0) 

    max_energy = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 1:
                return -1
            elif grid[r][c] == 3:
                max_energy = max(max_energy, seen.get((r,c), -1))

    return max_energy



