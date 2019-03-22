import randomplayer as player
import game
import pypokerengine.engine.action_checker as action_checker
import pypokerengine.utils.card_utils # estimate_hole_card_win_rate, evaluate hand

#DOESNT WORKKKKKK

class MinMaxAgent(player):
    """
    A computer player implementing the Min Max algorithm.
    This player behaves deterministically. That is, for a scenario, the player will always make the same
    move, even if other moves with the same evaluation exist.
    Already evaluated board positions are cached for efficiency.
    """

    WIN_VALUE = 1 # Winning pot.
    DRAW_VALUE = 0 # Split pot (Same card values)
    LOSS_VALUE = -1 # Losing pot.

    def __init__(self):
        """
        Getting ready for playing heads up limit hold'em.
        """
        self.side = None
        """
        Cache to store the evaluation of board positions that we have already looked at. This avoids repeating a lot
        of work as we do not look at all the possible continuation from this position again.
        """
        self.cache = {}
        super().__init__()

    def new_game(self, side: int):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        if self.side != side:
            self.side = side
            self.cache = {}

    def final_result(self, result: game):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    def _min(self, game: game) -> (float, int):
        """
        Evaluate the board position `board` from the Minimizing player's point of view.
        :param game: The board position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this board position before, and if yes just return the cached value
        #
        game_hash = game.hash_value()
        if game_hash in self.cache:
            return self.cache[game_hash]

        #
        # Init the min value as well as action. Min value is set to DRAW as this value will pass through in case
        # of a draw
        #
        min_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = game.who_won()
        if winner == self.side:
            min_value = self.WIN_VALUE
            action = -1
        elif winner == game.other_side(self.side):
            min_value = self.LOSS_VALUE
            action = -1
        else:
            for index in [i for i, e in enumerate(game.state) if game.state[i] == EMPTY]:
                b = game(game.state)
                b.move(index, game.other_side(self.side))

                res, _ = self._max(b)
                if res < min_value or action == -1:
                    min_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    if min_value == self.LOSS_VALUE:
                        self.cache[game_hash] = (min_value, action)
                        return min_value, action

                self.cache[game_hash] = (min_value, action)
        return min_value, action

    def _max(self, game: game) -> (float, int):
        """
        Evaluate the board position `board` from the Maximizing player's point of view.
        :param game: The board position to evaluate
        :return: Tuple of (Best Result, Best Move in this situation). Returns -1 for best move if the game has already
        finished
        """

        #
        # First we check if we have seen this board position before, and if yes just return the cached value
        #
        game_hash = game.hash_value()
        if game_hash in self.cache:
            return self.cache[game_hash]

        #
        # Init the min value as well as action. Min value is set to DRAW as this value will pass through in case
        # of a draw
        #
        max_value = self.DRAW_VALUE
        action = -1

        #
        # If the game has already finished we return. Otherwise we look at possible continuations
        #
        winner = game.who_won()
        if winner == self.side:
            max_value = self.WIN_VALUE
            action = -1
        elif winner == game.other_side(self.side):
            max_value = self.LOSS_VALUE
            action = -1
        else:
            for index in [i for i, e in enumerate(game.state) if game.state[i] == EMPTY]:
                b = game(game.state)
                b.move(index, self.side)

                res, _ = self._min(b)
                if res > max_value or action == -1:
                    max_value = res
                    action = index

                    # Shortcut: Can't get better than that, so abort here and return this move
                    if max_value == self.WIN_VALUE:
                        self.cache[game_hash] = (max_value, action)
                        return max_value, action

                self.cache[game_hash] = (max_value, action)
        return max_value, action

    def move(self, game: game) -> (game, bool):
        """
        Making a move according to the MinMax algorithm
        :param game: The board to make a move on
        :return: The result of the move
        """
        score, action = self._max(game)
        _, res, finished = game.move(action, self.side)
        return res, finished