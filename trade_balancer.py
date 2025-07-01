from itertools import combinations

# read a team's CSV and make a list of player options
# each player has name, rating, salary in millions, and contract years
def read_roster(path):
    roster = []
    with open(path) as f:
        next(f)
        for line in f:
            # split each line into parts
            name, rat, sal, yrs = [x.strip() for x in line.split(',')]
            rating = int(rat)
            salary = float(sal.replace('$','').replace('m',''))
            contract = int(yrs.replace('y',''))
            roster.append({
                'name': name,
                'rating': rating,
                'salary': salary,
                'contract': contract
            })
    return roster

# score how good a trade is for your team
# we look at rating gain, salary efficiency, and rookie cost
def score_trade(give_group, get_group):
    # calculate rating gain (you get minus you give)
    sum_give = sum(p['rating'] for p in give_group)
    sum_get  = sum(p['rating'] for p in get_group)
    rating_gain = sum_get - sum_give

    # calculate efficiency (rating per salary)
    give_sal = sum(p['salary'] for p in give_group)
    get_sal  = sum(p['salary'] for p in get_group)
    eff_give = sum_give / give_sal
    eff_get  = sum_get  / get_sal
    efficiency_gain = eff_get - eff_give

    # find rookies (cheap but high rating is the give away) and apply penalty
    rookies = [p['name'] for p in get_group
               if p['contract'] >= 3 and p['salary'] < p['rating']]
    rookie_penalty = len(rookies) * 4

    # combine into a score (lower is better for you)
    score = (-rating_gain) + (-efficiency_gain * 5) + rookie_penalty
    details = {
        'rating_gain': rating_gain,
        'efficiency_gain': efficiency_gain,
        'rookies': rookies
    }
    return score, details

# find the best trade of give_n vs get_n players
def find_best_trade(teamA, teamB, give_n, get_n):
    best = None
    best_score = float('inf')
    # try every combination of players
    for give_group in combinations(teamA, give_n):
        for get_group in combinations(teamB, get_n):
            score, details = score_trade(give_group, get_group)
            if score < best_score:
                best_score = score
                best = (give_group, get_group, details)
    return best