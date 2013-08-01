from itertools import combinations
import random


class Player(object):

    def __init__(self, strategy, name=None):
        self.strategy = strategy
        self.hunts = 0
        self.slacks = 0
        self.name = name if name \
            else getattr(strategy, '__name__', str(strategy))

    @property
    def reputation(self):
        rounds = self.hunts + self.slacks
        return 1.0 * self.hunts / rounds if rounds > 0 else 0

    def hunt_choices(self, *args):
        return self.strategy.hunt_choices(*args)

    def hunt_outcomes(self, *args):
        return self.strategy.hunt_outcomes(*args)

    def round_end(self, *args):
        return self.strategy.round_end(*args)

    def __repr__(self):
        return "%s[food: %s, rep: %.2f]" % (self.name, self.food,
                                            self.reputation)


class Game(object):

    def __init__(self, strategies):
        self.strategies = strategies

    def earn_food(self, player, a1, a2):
        food = 0
        if a1 == 'h':
            self.hunt_c += 1
            player.hunts += 1
            food -= 3
        else:
            player.slacks += 1
            food -= 2
        if a2 == 'h':
            food += 3
        return food

    def hunt(self, p1, p2):
        a1 = self.choices[p1][p2]
        a2 = self.choices[p2][p1]
        # print "%s[%s] VS %s[%s]" % (pp(p1), a1, pp(p2), a2)
        self.food_earned[p1][p2] += self.earn_food(p1, a1, a2)
        self.food_earned[p2][p1] += self.earn_food(p2, a2, a1)

    def play_round(self):
        ps = len(self.players)
        m = random.randint(1, (ps * ps - 1) - 1)
        self.round_n += 1
        self.hunt_c = 0
        self.choices = {}
        self.food_earned = {}
        # print "Round: %d" % self.round_n
        # print "Players: %s" % ", ".join([str(p) for p in self.players])
        # print "Award given at: %d hunts" % m

        # Calculate actions
        for player in self.players:
            others = [p for p in self.players if p != player]
            random.shuffle(others)
            self.food_earned[player] = dict(zip(others, [0] * len(others)))
            self.choices[player] = dict(zip(others, player.hunt_choices(
                self.round_n, player.food, player.reputation, m,
                map(lambda x: x.reputation, others))))
        # Perform actions
        for (p1, p2) in combinations(self.choices, 2):
            self.hunt(p1, p2)

        bonus = 0
        if self.hunt_c >= m:
            bonus = 2 * (ps - 1)
            # print "  AWARD[%d]: %d" % (self.round_n, bonus)

        for player in self.players:
            # print "%s earned food: %r, bonus: %d" % (
            #    pp(player), self.food_earned[player].values(), bonus)
            player.food += sum(self.food_earned[player].values()) + bonus
            player.hunt_outcomes(self.food_earned[player])
            player.round_end(bonus, m, self.hunt_c)

        starved = [p for p in self.players if p.food <= 0]
        if starved:
            print "  STARVED[%d]: %r" % (self.round_n,
                                         [p for p in starved])
            self.players = [p for p in self.players if p.food > 0]

    def play_game(self):
        self.round_n = 0

        # Set up players
        self.players = []
        for strategy in self.strategies:
            player = Player(strategy)
            player.food = 300 * (len(self.strategies) - 1)
            self.players.append(player)

        print "PLAYERS: %r" % [p for p in self.players]
        max_rounds = 5000
        last_players = []

        while len(self.players) > 1 and self.round_n < max_rounds:
            last_players = self.players
            self.play_round()

        if len(self.players) == 0:
            self.players = last_players

        print "Left: %r" % self.players
        winners = sorted(self.players, key=lambda p:
                         p.food + p.reputation,
                         reverse=True)
        winners = [w for w in winners if w.food + w.reputation == winners[
            0].food + winners[0].reputation]
        print "WINNER[%d]: %r\n" % (self.round_n, winners)
        return winners


if __name__ == '__main__':
    from players import *

    players = [always, never, alternate]
    game = Game(players)
    "Winner(s): %r" % game.play_game()
