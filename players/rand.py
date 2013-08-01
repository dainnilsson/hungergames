import random


def hunt_choices(round_number, current_food, current_reputation, m,
                 player_reputations):

    hunt_decisions = [
        'h' if random.random() > 0.5 else 's' for x in player_reputations]
    return hunt_decisions


def hunt_outcomes(food_earnings):
    pass  # do nothing


def round_end(award, m, number_hunters):
    pass  # do nothing


class Player:

    def __init__(self, chance=0.5):
        self.chance = chance

    def hunt_choices(self, round_number, current_food, current_reputation, m,
                     player_reputations):
        hunt_decisions = ['h' if random.random() < self.chance
                          else 's' for x in player_reputations]
        return hunt_decisions

    def hunt_outcomes(self, *args):
        return hunt_outcomes(*args)

    def round_end(self, *args):
        return round_end(*args)

    def __repr__(self):
        return "Random(%.2f)" % self.chance
