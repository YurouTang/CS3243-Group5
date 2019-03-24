from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, _montecarlo_simulation, estimate_hole_card_win_rate

class MonteCarloPlayer(BasePokerPlayer):
    def __init__(self):
        self.wins = 0
        self.losses = 0

    def declare_action(self, valid_actions, hole_card, round_state):
        # Estimate the win rate
        win_rate = estimate_hole_card_win_rate(100, self.num_players, gen_cards(hole_card), gen_cards(round_state['community_card']))

        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        
        # If the win rate is large enough, then raise
        if win_rate > 0.5:
            if win_rate > 0.75:
                # If it is extremely likely to win, then raise
                action = 'raise'
            else:
                # If there is a chance to win, then call
                action = 'call'
        else:
            action = 'call' if can_call else 'fold'

        return action

    def receive_game_start_message(self, game_info):
        self.num_players = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)


def setup_ai():
    return DataBloggerBot()