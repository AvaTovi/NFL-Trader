import os
from trade_balancer import read_roster, find_best_trade, score_trade

# show a menu to pick a team from the list
def pick_team(prompt, teams):
    print(prompt)
    for i, t in enumerate(teams, 1):
        print(f"{i}. {t}")
    while True:
        choice = input("Enter number: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(teams):
                return teams[idx]
        print("Invalid, please pick a number from the list.")

# This will display the roster of a team in a readable format
def display_roster(name, roster):
    print(f"\n{name} roster:")
    for i, p in enumerate(roster, 1):
        print(f"{i}. {p['name']} | OVR {p['rating']} | ${p['salary']}m | {p['contract']}y")

# let user pick which players they want to trade
def get_choices(count, size):
    picks = []
    while len(picks) < size:
        choice = input(f"Pick player #{len(picks)+1}: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < count and idx not in picks:
                picks.append(idx)
                continue
        print("Invalid choice, try again.")
    return picks

# evaluate the manual player selection
def evaluate_manual_trade(teamA, teamB, a_idx, b_idx):
    give_group = [teamA[i] for i in a_idx]
    get_group  = [teamB[i] for i in b_idx]
    score, details = score_trade(give_group, get_group)
    return give_group, get_group, details

# main program flow
def main():
    # get all team names from the rosters folder
    files = [f for f in os.listdir('rosters') if f.endswith('.csv')]
    teams = [f[:-4] for f in files]

    # pick your team and opponents team
    my_team  = pick_team("Pick your team:", teams)
    opp_team = pick_team("Pick opponent team:", [t for t in teams if t != my_team])

    # read both rosters from CSV
    rosterA = read_roster(f'rosters/{my_team}.csv')
    rosterB = read_roster(f'rosters/{opp_team}.csv')

    # show both rosters
    display_roster(my_team, rosterA)
    display_roster(opp_team, rosterB)

    # ask how many players to trade
    give_n = int(input("\nHow many you give? (1 or 2): "))
    get_n  = int(input("How many you get? (1 or 2): "))

    # pick players by number for give and get
    print(f"\nSelect {give_n} player(s) you give:")
    a_idx = get_choices(len(rosterA), give_n)
    print(f"\nSelect {get_n} player(s) you get:")
    b_idx = get_choices(len(rosterB), get_n)

    # evaluate and get trade details
    give_group, get_group, details = evaluate_manual_trade(rosterA, rosterB, a_idx, b_idx)

    # show trade result
    print("\nYou give:")
    for p in give_group:
        print(f" - {p['name']} (OVR {p['rating']})")

    print("You get:")
    for p in get_group:
        print(f" - {p['name']} (OVR {p['rating']})")

    # print the computed gains and rookie warning
    print(f"\nRating gain: {details['rating_gain']}")
    print(f"Efficiency gain: {details['efficiency_gain']:.2f}")
    if details['rookies']:
        print("⚠ Rookie(s):", ", ".join(details['rookies']))

    # final verdict just for you
    rg = details['rating_gain']
    eg = details['efficiency_gain']
    if rg >= 5 and eg >= 0:
        print("Great deal for you")
    elif rg >= 0:
        print("Decent deal for you")
    else:
        print("Bad deal for you")

# start program
if __name__ == '__main__':
    main()