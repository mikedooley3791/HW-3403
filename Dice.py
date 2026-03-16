# region imports #Region start for imports
from Die import rollFairDie, rollUnFairDie #imports functions for Die
# endregion #Region Ends for imports

# region functions
def rollFairDice(N=1):
    """
    This function simulates rolling N dice simultaneously by using a loop that rolls
    a single die N times and totaling the score.
    :param N: the number of dice to be rolled
    :return: the total score from rolling N dice
    """
    score = 0
    for i in range(N):
        score += rollFairDie()
    return score

def rollUnFairDice(N=1):
    """
    This function simulates rolling N, UnFair dice simultaneously by using a loop that rolls
    a single die N times and totals the score.
    :param N: the number of dice to be rolled
    :return: the total score from rolling N dice
    """
    score = 0
    for i in range(N):
        score += rollUnFairDie()
    return score
# endregion