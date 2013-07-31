last_played = 's'

def hunt_choices(round_number, current_food, current_reputation, m,
            player_reputations):

    global last_played
    
    hunt_decisions = list()
    for reputation in player_reputations:
        last_played = 's' if last_played == 'h' else 'h'
        hunt_decisions.append(last_played)     
    return hunt_decisions

def hunt_outcomes(food_earnings):
    pass # do nothing

def round_end(award, m, number_hunters):
    pass # do nothing