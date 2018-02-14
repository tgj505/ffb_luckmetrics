import numpy as np

"""
# Weekly variables
points_rank = input("Weekly points rank: ")
number_of_teams = input("Number of teams: ")
result = input("Result: ")

# Season total (so far): number_of_games, ; total_points_against, number_of_games
wins = input("Wins: ")
total_points = input("Season points: ")
league_avg_points = input("Average league points: ")
number_of_games = input("Games played so far: ")
total_points_against = input("Total points against: ")

## ********** I HAVEN'T IMPLEMENTED THE ABOVE YET! NEED TO ORGANIZE THIS

******
ASLDKJLAKSJD"""




# Metric #1: Weekly Luck
#   This essentially measures how lucky you are to win or lose a single game based on how many points you scored
#   For example, if you scored the second most points and lost, you'd have a weekly_luck of -1.
#   If you scored the second fewest points but still won, you'd have a weekly luck of 1.
#   If you score the most or least points, your luck will be 0.
#   If you tie, your luck will basically just be halved
#   This is the bread-and-butter luck metric since it directly measures one aspect of your skill (points)
#       against one measure of your luck (wins).
def weekly_luck(number_of_teams, points_rank, result):
    eW = (points_rank - 1)/(number_of_teams - 1) # "Expected win", or what was your likelihood of winning
    if result == "t":
        luck = 1 / 2 - eW
    elif eW == 1 or 0:
        luck = 0
    elif result == "l":
        luck = -eW
    elif result == "w":
        luck = 1-eW
    return luck
# Testing
# tom_test = weekly_luck(14, 9, 'w')
# print("weekly luck:", tom_test)


# Metric #2: Raw Points to Wins
#   This is an inelegant measure that's similar to weekly luck. Basically, it takes how many points you've scored
#       and compares to your win total. It's very crude, but an easy measure of points-to-wins.
#   If you have scored the most points in the league, you would be expected to have won all your games.
#   If you have won the least, you would be expected to lose all of your games.
#   This metric just spits out a number wins above or below your expected number.
def raw_points_to_win(points_rank, number_of_teams, number_of_games, wins):
    rp_luck = wins - (number_of_games * ((points_rank)/number_of_teams))
    rp_luck /= number_of_games
    return rp_luck

# Testing
#tom_test = raw_points_to_win(5, 14, 3, 3)
# print("raw_points luck: ", tom_test)


# Metric #3: Weighted Points to Wins
#   This is a slightly better version of the above since it takes the deviation of your points from avg into account
#   So, it's not just a ranking of points, but based on a weighted ranking.
#   If you're the leading scorer, but you're close to avg, you'll be a little lucky to win a ton of games, rather
#       than not at all lucky in the metric above.
#   If you score the fewest points, but not by much, you'll be less lucky to win more games
def weighted_points_to_win(points, league_avg_points, number_of_games, wins):
    point_ratio = (points/league_avg_points)
    # Scales the points to expected wins
    # expected_wins = number_of_games * np.tanh((point_ratio - 1)*2) + number_of_games/2
    expected_win_ratio = (point_ratio**number_of_games)/(1+point_ratio**number_of_games)
    # print('expected_wins:', expected_win_ratio)
    expected_wins = expected_win_ratio * number_of_games
    # print('expected_wins:', expected_wins)
    wp_luck = (-1)*(expected_wins - wins)
    return wp_luck

# Testing
tom_test = weighted_points_to_win(1607.5, 1484, 13, 8)
# print("wp_luck:", tom_test)


# Just following pro-football seciton of: https://en.wikipedia.org/wiki/Pythagorean_expectation
# Probably need to mess around with the exponents since points will be much higher in fantasy
# I've decided to use exponents that Hollinger uses for NBA: 16.5, since scores in FFB are closer to basketball than fb
# This is in many ways the most simple kind of luck
def pythagorean_total(total_points, total_points_against, number_of_games, wins):
    pythag_ratio = ((total_points**16.5)/((total_points**16.5 )+(total_points_against**16.5)))
    # print("pythag_ratio:", pythag_ratio)
    pythag_expect = pythag_ratio * number_of_games
    # print("pythag_expect:", pythag_expect)
    pythag_luck = wins - pythag_expect
    # print("pythag_luck:", pythag_luck)
    return pythag_luck

# tom_test = pythagorean_total(1607.5, 1485.3, 13, 8)

