from src.Board import Board
from src.Colour import Colour
from random import uniform


class State:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = Board(board_size)
        # the player who needs to take action now
        self.next_player = Colour.RED

    def get_winner(self):
        """
        If the game has ended, return the winner. If not, return None.
        """
        if self.board.has_ended():
            # Colour.RED or Colour.BLUE
            return self.board.get_winner()
        else:
            return None
        
    def play(self, move):
        """
        Place a stone on the board.
        """
        self.board.set_tile_colour(move[0], move[1], self.next_player)
        # indicate the next player who will make a move
        self._next_turn()
    
    def swap(self):
        lower = self.board_size * 0.25
        upper = self.board_size * 0.75
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board._tiles[i][j].colour is not None:
                    if lower < i < upper and lower < j < upper:
                        return True
        return False

    def play_first_move(self):
        lower = self.board_size * 0.25
        upper = self.board_size * 0.75
        x = int(uniform(lower, upper))
        y = int(uniform(lower, upper))

        self.play((x, y))
        return (x, y)
        

    def _next_turn(self):
        if self.next_player == Colour.RED:
            self.next_player = Colour.BLUE
        elif self.next_player == Colour.BLUE:
            self.next_player = Colour.RED

    def get_valid_moves(self):
        """
        Return a list of valid movements.
        """
        valid_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board._tiles[i][j].colour is None:
                    valid_moves.append((i, j))
        return valid_moves

if __name__ == '__main__':
    state = State(2)
    print(state.get_valid_moves())