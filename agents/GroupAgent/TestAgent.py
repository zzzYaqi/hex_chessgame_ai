import socket
from random import choice
from time import sleep
from State import State
from TestRave import TestRaveMCTS

class TestAgent():
    """This class describes the default Hex agent. It will randomly send a
    valid move at each turn, and it will choose to swap with a 50% chance.
    """

    HOST = "127.0.0.1"
    PORT = 1234

    def __init__(self, board_size=11):
        self.s = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        self.s.connect((self.HOST, self.PORT))

        self.board_size = board_size
        # self.board = []
        self.colour = ""
        self.turn_count = 0
        self.gameState = State(board_size)
        


    def run(self):
        """Reads data until it receives an END message or the socket closes."""

        while True:
            data = self.s.recv(1024)
            if not data:
                break
            # print(f"{self.colour} {data.decode('utf-8')}", end="")
            if (self.interpret_data(data)):
                break
        
        self._close()
        # print(f"Naive agent {self.colour} terminated")

    def interpret_data(self, data):
        """Checks the type of message and responds accordingly. Returns True
        if the game ended, False otherwise.
        """

        messages = data.decode("utf-8").strip().split("\n")
        messages = [x.split(";") for x in messages]
        # print(messages)
        for s in messages:
            if s[0] == "START":
                # update board size
                self.board_size = int(s[1])
                self.gameState = State(self.board_size)
                self.colour = s[2]
                # self.board = [
                #     [0]*self.board_size for i in range(self.board_size)]

                if self.colour == "R":
                    self.make_move()

            elif s[0] == "END":
                return True

            elif s[0] == "CHANGE":
                if s[3] == "END":
                    return True
                
                elif s[1] == "SWAP":
                    self.colour = self.opp_colour()
                    if s[3] == self.colour:
                        self.make_move()

                elif s[3] == self.colour:
                    # action = [int(x) for x in s[1].split(",")]
                    # self.board[action[0]][action[1]] = self.opp_colour()

                    # opponent made a move and update the game state
                    move = s[1].split(',')
                    self.gameState.play((int(move[0]),int(move[1])))

                    self.make_move()

        return False

    def make_move(self):
        """Makes move  
        """

        # print(f"{self.colour} making move")
        if self.colour == "B" and self.turn_count == 0:
            if self.gameState.swap():
                self.s.sendall(bytes("SWAP\n", "utf-8"))
                print('*************')
                print('swap')
            else:
                # get the best move from mcts search
                mcts = TestRaveMCTS(self.gameState)
                move = mcts.get_best_move()
                self.s.sendall(bytes(f"{move[0]},{move[1]}\n", "utf-8"))
                # update game state
                self.gameState.play((move[0],move[1]))
                print('*************')
                print('move:', move, self.colour)
                # self.board[move[0]][move[1]] = self.colour

        # if we are red and need to make the first move, choose a certain area on the board
        # in case we are swapped
        elif self.colour == "R" and self.turn_count == 0:
            move = self.gameState.play_first_move()
            self.s.sendall(bytes(f"{move[0]},{move[1]}\n", "utf-8"))


        else:
            # now we need to make move, use mcts to get a best move and get the position to send the message
            mcts = TestRaveMCTS(self.gameState)
            move = mcts.get_best_move()
            # move = [3,3]
            self.s.sendall(bytes(f"{move[0]},{move[1]}\n", "utf-8"))
            # update game state
            self.gameState.play((move[0],move[1]))
            print('*************')
            print('move:', move, self.colour)
            # self.board[move[0]][move[1]] = self.colour

        self.turn_count += 1

    def _close(self):
        """Closes the socket."""

        self.s.close()
        return 0
    
    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """
        if self.colour == "R":
            return "B"
        elif self.colour == "B":
            return "R"
        else:
            return "None"
    
if (__name__ == "__main__"):
    agent = TestAgent()
    agent.run()
