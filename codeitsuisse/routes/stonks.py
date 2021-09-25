import logging
import json
from collections import defaultdict

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stonks', methods=['POST'])
def stonks():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    ans = []
    for test_case in data:
        seq = []
        energy = test_case.get("energy")
        capital = test_case.get("capital")
        timeline = test_case.get("timeline")
        companies = defaultdict(list)
        # naive as fucking fuck
        for year in timeline:
            for company in timeline[year]:
                companies[company].append((timeline[year][company]["price"], year))
        high = 0
        best = None
        best_company = None
        for company in companies:
            companies[company].sort(key = lambda x: x[0])
            diff = companies[company][-1][0] - companies[company][0][0]
            if diff > high:
                best = (companies[company][-1], companies[company][0])
                best_company = company
                high = diff
        end = best[0][1]
        start = best[1][1]
        print(start, end)
        
        to_start = 2037 - int(start)
        to_end = 2037 - int(end)
        remaining_energy = energy - to_start - to_end
        to_travel = abs(int(start) - int(end))
        if remaining_energy < to_travel or to_travel == 0:
            print('fked iup')
            return json.dumps(0)
        
            # xd fk this shit lmao xdxd
        
        # 2037 to start
        max_start = 0
        start_company = None
        if "2037" in timeline.keys():
            companies = set(timeline["2037"].keys()).union(set(timeline[start].keys()))
            for company in companies:
                buy = timeline[start][company]["price"] - timeline["2037"][company]["price"]
                if buy > max_start:
                    start_company = company
                    max_start = buy
        # print(max_start, "max start")
        if max_start > 0:
            max_buy = min(capital // timeline['2037'][start_company]["price"], timeline['2037'][start_company]["qty"]) 
            timeline['2037'][start_company]["qty"] -= max_buy
            cost = max_buy * timeline['2037'][start_company]["price"]
            seq.extend([f'b-{start_company}-{max_buy}', f'j-2037-{start}', f's-{start_company}-{max_buy}'])
            profit = max_buy * timeline[start][start_company]["price"]
            capital = capital + profit - cost
        else:
            seq.append(f'j-2037-{start}')
        
        energy -= to_start
        energy -= to_end
        
        # forward
        energy -= to_travel
        max_buy = min(capital // timeline[start][best_company]["price"], timeline[start][best_company]["qty"]) 
        timeline[start][best_company]["price"] -= max_buy
        cost = max_buy * timeline[start][best_company]["price"]
        profit = max_buy * timeline[end][best_company]["price"]
        capital = capital + profit - cost
        seq.extend([f'b-{best_company}-{max_buy}', f'j-{start}-{end}', f's-{best_company}-{max_buy}'])

        if energy >= (2*to_travel):
            # find best end to start
            # repeat that shitttt
            max_back = 0
            back_company = None
            companies = set(timeline[end].keys()).union(set(timeline[start].keys()))
            for company in companies:
                buy = timeline[start][company]["price"] - timeline[end][company]["price"]
                if buy > max_back:
                    back_company = company
                    max_back = buy
            while energy >= (2*to_travel):
                # break
                # back
                if max_back > 0:
                    energy -= to_travel
                    max_buy = min(capital // timeline[end][back_company]["price"], timeline[end][back_company]["qty"]) 
                    timeline[end][back_company]["price"] -= max_buy
                    cost = max_buy * timeline[end][back_company]["price"]
                    profit = max_buy * timeline[start][back_company]["price"]
                    capital = capital + profit - cost
                    seq.extend([f'b-{back_company}-{max_buy}', f'j-{end}-{start}', f's-{back_company}-{max_buy}'])
                else:
                    seq.append(f'j-{end}-{start}')
                    energy -= to_travel
                    
                # forward again
                energy -= to_travel
                max_buy = min(capital // timeline[start][best_company]["price"], timeline[start][best_company]["qty"]) 
                timeline[start][best_company]["price"] -= max_buy
                cost = max_buy * timeline[start][best_company]["price"]
                profit = max_buy * timeline[end][best_company]["price"]
                capital = capital + profit - cost
                seq.extend([f'b-{best_company}-{max_buy}', f'j-{start}-{end}', f's-{best_company}-{max_buy}'])

                # 2037 to start
        max_end = 0
        end_company = None
        if "2037" in timeline.keys():
            companies = set(timeline["2037"].keys()).union(set(timeline[end].keys()))
            for company in companies:
                buy = timeline['2037'][company]["price"] - timeline[end][company]["price"]
                if buy > max_end:
                    end_company = company
                    max_end = buy
        if max_end > 0:
            max_buy = min(capital // timeline[end][end_company]["price"], timeline[end][end_company]["qty"]) 
            timeline[end][end_company]["qty"] -= max_buy
            cost = max_buy * timeline[end][end_company]["price"]
            seq.extend([f'b-{end_company}-{max_buy}', f'j-{end}-2037', f's-{end_company}-{max_buy}'])
            profit = max_buy * timeline[start][end_company]["price"]
            capital = capital + profit - cost
        else:
            seq.append(f'j-{end}-2037')
        ans.append(seq)
        
        
        
    return json.dumps(seq)



