import State
from math import sqrt, log
from copy import deepcopy
from random import choice
from time import time

class Node:
    def __init__(self, move=None, parent=None):
        self.move = move
        self.parent = parent
        self.N = 0  # num of times the node is visited
        self.Q = 0  # average reward of the node
        # self.N_RAVE = 0
        # self.Q_RAVE = 0
        self.children = {}
        # self.outcome = None

    def add_children(self, children):
        for child in children:
            self.children[child.move] = child

    
    @property
    def value(self, explore=0.1):
        # The value of explore should be MCTSMeta.EXPLORATION
        if self.N == 0:
            return 0 if explore == 0 else float('inf')
        else:
            return self.Q / self.N + explore * sqrt(2 * log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, gameState):
        self.root_state = deepcopy(gameState)
        self.root_node = Node()
        # times of simulation
        self.sim_num = 0
        self.time_limit = 2

    def get_best_move(self):
        self._controller()
        return self._get_best_node(self.root_node).move

    def _controller(self):
        start = time()
        while time() - start < self.time_limit:

            curr_node, curr_state = self._select()
            # for curr_node: 1)hasn't been visited (N=0) or 2)game ended
            if curr_state.get_winner() is None:
                winner = self._simulate(curr_state)
            else:
                winner = curr_state.get_winner()
            # based on the next player and the winner, do the back propagation
            self._back_prop(curr_node, curr_state.next_player, winner)
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
            children.append(Node(move, parent))
        parent.add_children(children)

    def _simulate(self, state):
        # this list needs to be a list of tuple
        valid_moves = state.get_valid_moves()
        while state.get_winner() is None:
            move = choice(valid_moves)
            state.play(move)
            valid_moves.remove(move)

        return state.get_winner()
    
    def _back_prop(self, node, player, winner):
        reward = 0 if player == winner else 1
        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            reward = 0 if reward == 1 else 1
