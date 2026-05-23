import State
from src.Colour import Colour
from math import sqrt, log
from copy import deepcopy
from random import choice
from time import time

class RaveNode:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.N = 0  # num of times the node is visited
        self.Q = 0  # num of wins (win: +1 reward, loss: 0 reward)
        self.N_rave = 0
        self.Q_rave = 0
        self.children = {}

    def add_children(self, children):
        for child in children:
            self.children[child.move] = child
    
    @property
    def value(self, explore=0.1, rave_const=300):
        # explore: should be tuned
        # rave_const: number of visits a node will have before RAVE score is not used at all
        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else:
            # RAVE score with UCT
            UCT =  self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)
            alpha = max(0, (rave_const - self.N) / rave_const)
            RAVE = self.Q_rave / self.N_rave if self.N_rave != 0 else 0
            return alpha * RAVE + (1 - alpha) * UCT


class RaveMCTS:
    def __init__(self, gameState):
        self.root_state = deepcopy(gameState)
        self.root_node = RaveNode()
        # times of simulation
        self.sim_num = 0
        self.time_limit = 2  # in seconds

    def get_best_move(self):
        self._controller()
        return self._get_best_node(self.root_node).move

    def _controller(self):
        start = time()
        while time() - start < self.time_limit:
            curr_node, curr_state = self._select()
            # for curr_node: 1)hasn't been visited (N=0) or 2)game ended
            winner, red_moves, blue_moves = self._simulate(curr_state)
            # based on the next player and the winner, do the back propagation
            self._back_prop(curr_node, curr_state.next_player, winner, red_moves, blue_moves)
            self.sim_num += 1
        print(self.sim_num)

    def _select(self):
        node = self.root_node
        state = deepcopy(self.root_state)
        
        # get the node with the max value of the children of the node
        while len(node.children) != 0: # if this node has children
            # get the max value of the children of this node
            selected_child = self._get_best_node(node)
            # update current state and node
            node = selected_child
            state.play(node.move)
            # if the N is 0, return and do roll out
            if node.N == 0:
                return node, state
            
        # if node has no children and is not leaf, add children to the node
        if state.get_winner() is None:
            self._expand(node, state)
            # update current state and node
            node = choice(list(node.children.values()))
            state.play(node.move)

        return node, state
    

    def _get_best_node(self, node):
        children = node.children.values()
        max_value = max(children, key=lambda n: n.value).value
        best_children = [child for child in children if child.value == max_value]    
        return choice(best_children)
    

    def _expand(self, parent, state):
        children = []
        for move in state.get_valid_moves():
            children.append(RaveNode(move, parent))
        parent.add_children(children)

    def _simulate(self, state):
        """
        Rollout phase. Record the moves played during rollout, and their corresponding colour.
        """
        # if game ended, no need for rollout, return the winner
        if state.get_winner() is not None:
            return (state.get_winner(), [], [])

        # # this list needs to be a list of tuple
        # valid_moves = state.get_valid_moves()
        # while state.get_winner() is None:
        #     move = choice(valid_moves)
        #     state.play(move)
        #     valid_moves.remove(move)
        
        # # store the tuples played in rollout
        # red_moves = []
        # blue_moves = []
        # # check all the tiles on the board?
        # for i in range(state.size):
        #     for j in range(state.size):
        #         if state.board._tiles[i][j].colour == Colour.RED:
        #             red_moves.append((i, j))
        #         elif state.board._tiles[i][j].colour == Colour.BLUE:
        #             blue_moves.append((i, j))

        red_moves = []
        blue_moves = []
        valid_moves = state.get_valid_moves()
        while state.get_winner() is None:
            move = choice(valid_moves)
            # add the move and colour to the list
            colour = state.next_player
            if colour == Colour.RED:
                red_moves.append(move)
            elif colour == Colour.BLUE:
                blue_moves.append(move)
            state.play(move)
            valid_moves.remove(move)

        return (state.get_winner(), red_moves, blue_moves)
    
    def _back_prop(self, node, next_player, winner, red_moves, blue_moves):
        # if player1 made a move and winner is player2 (the next player), then the reward for player1 is 0
        reward = 0 if next_player == winner else 1

        while node is not None:
            # update RAVE
            if next_player == Colour.RED:
                for move in red_moves:
                    if move in node.children:
                        node.children[move].N_rave += 1
                        # children's reward is opposite from parent
                        node.children[move].Q_rave += 0 if reward == 1 else 1
            else:  # for BLUE
                for move in blue_moves:
                    if move in node.children:
                        node.children[move].N_rave += 1
                        node.children[move].Q_rave += 0 if reward == 1 else 1
            # update UCT
            node.N += 1
            node.Q += reward

            node = node.parent
            # update next_player for the parent node
            next_player = Colour.RED if next_player == Colour.BLUE else Colour.BLUE
            reward = 0 if reward == 1 else 1
