from pypokerengine.players import BasePokerPlayer
import random as rand
import pprint
import pypokerengine.engine.action_checker as action_checker
import pypokerengine.utils.card_utils # estimate_hole_card_win_rate, evaluate hand

# class State:

    # Always call pre-flop (chances of making hands much better in a pot-limit setting)
    # Money in the pot (pot odds) 0.3
    # Strength of hand vs expected his hands 0.5
    # Behavior (history - probably the hardest, indication of aggressive vs passive player) 0.1
    # Tendency for our player to be 'loose' 0.1
    # Fold if < 0.3?
    # Call if >= 0.3 && < 0.7
    # Bet/Raise if >=0.7

class Group05(BasePokerPlayer):
  def declare_action(self, valid_actions, hole_card, round_state):
    # valid_actions format => [raise_action_pp = pprint.PrettyPrinter(indent=2)
    pp = pprint.PrettyPrinter(indent=2)
    print("------------ROUND_STATE(RANDOM)--------")
    pp.pprint(round_state)
    print("------------HOLE_CARD----------")
    pp.pprint(hole_card)
    print("------------VALID_ACTIONS----------")
    pp.pprint(valid_actions)
    print("-------------------------------")
    if round_state == 'preflop':
        call_action_info = valid_actions[1]

    r = rand.random()
    if r <= 0.5:
      call_action_info = valid_actions[1]
    elif r<= 0.9 and len(valid_actions ) == 3:
      call_action_info = valid_actions[2]
    else:
      call_action_info = valid_actions[0]
    action = call_action_info["action"]
    return action  # action returned here is sent to the poker engine

  def receive_game_start_message(self, game_info):
    pass

  def receive_round_start_message(self, round_count, hole_card, seats):
    pass

  def receive_street_start_message(self, street, round_state):
    pass

  def receive_game_update_message(self, action, round_state):
    pass

  def receive_round_result_message(self, winners, hand_info, round_state):
    pass

def setup_ai():
  return Group05()
