import csv
import math

TEAMS_FILENAME = "nalcs/data/2017/teams.csv"
SPRING_FILENAME = "nalcs/data/2017/spring_matches.csv"

INITIAL_RATING = 1500
LOGISTIC_PARAMETER = 400




def expected_outcome(team_1_rating, team_2_rating):
    """
    Given two predictions' elo ratings, return the likelihood of the first winning.

    This is basically how elo ratings work, uses a logistic curve.
    """
    return 1 / (1 + math.pow(10, ((team_2_rating - team_1_rating) / LOGISTIC_PARAMETER)))


teams = {}
with open(TEAMS_FILENAME) as team_file:
    for row in csv.reader(team_file, delimiter=','):
        team_name = row[0]
        short = row[1]
        teams[short] = INITIAL_RATING

def run(k_factor):
    likelihood = 1.0

    for t in teams.keys():
        teams[t] = INITIAL_RATING

    with open(SPRING_FILENAME) as spring_file:
        for row in csv.reader(spring_file, delimiter=','):
            #print(row)
            team_1 = row[0]
            team_2 = row[1]
            wins_1 = int(row[2])
            wins_2 = int(row[3])

            # multiply in the likelihood
            p_win_1 = expected_outcome(teams[team_1], teams[team_2])
            likelihood_factor = math.pow(p_win_1, wins_1) * math.pow((1.0 - p_win_1), wins_2)
            default_likelihood =  math.pow(0.5, (wins_1 + wins_2))
            #print("likelihood: " + str(likelihood_factor) + ", default: " + str(default_likelihood))
            likelihood *= likelihood_factor
            likelihood /= default_likelihood

            # update ratings
            expected_team_1_wins = expected_outcome(teams[team_1], teams[team_2]) * (wins_1 + wins_2)
            expected_team_2_wins = expected_outcome(teams[team_2], teams[team_1]) * (wins_1 + wins_2)
            #print(team_1 + ": " + str(teams[team_1]) + " " + str(expected_team_1_wins))
            #print(team_2 + ": " + str(teams[team_2]) + " " + str(expected_team_2_wins))


            teams[team_1] += k_factor * (wins_1 - expected_team_1_wins)
            teams[team_2] += k_factor * (wins_2 - expected_team_2_wins)

            #print(team_1 + ": " + str(teams[team_1]))
            #print(team_2 + ": " + str(teams[team_2]))


        print("k factor: " + str(k_factor) + ": " + str(likelihood))

for i in range(1, 35, 1):
    run(i)