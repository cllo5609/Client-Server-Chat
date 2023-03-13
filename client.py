# Author: Clinton Lohr
# Date: 05/31/2022


"""
Sources:
(1) https://docs.python.org/3.4/howto/sockets.html
(2) https://realpython.com/python-sockets/
(3) Computer Networking: A Top Down Approach 8th edition, (Jim Kurose, Keith Ross)

"""

import socket


class TicTacToe:
    """
    Creates a TicTacToe Object. This class is responsible for initializing and creating a tic-tac-toe game board and
    tracking how many rounds have been played throughout the course of the game. Includes various methods for carrying
    out game play.
    """

    def __init__(self):
        """
        Initializes and creates a tic-tac-toe board and creates a variable for tracking the number of rounds played
        throughout the course of the game.
        """

        self.game_board = []
        self.create_board()
        self.round_count = 0

    def create_board(self):
        """
        Creates an empty 3x3 tic-tac-toe game board and appends each row of the board to self.game_board
        :return: NONE
        """

        for i in range(3):
            row = []
            for j in range(3):
                row.append("-")
            self.game_board.append(row)

    def print_board(self):
        """
        Prints the current game board to the command prompt or terminal
        :return: NONE
        """

        for i in range(3):
            print(self.game_board[i], "\n")

    def check_receive(self):
        """
        Checks if the client has received a response from the server. Received messages are decoded and returned.
        :return: Decoded message as a string
        """

        recv_message = client_socket.recv(2221)
        decoded_message = recv_message.decode()
        return decoded_message

    def send_message(self, message):
        """
        Receives a client created message. The message is encoded and sent to the server
        :param message: Represents the message created by the client
        :return: NONE
        """

        encoded_message = message.encode()
        client_socket.send(encoded_message)

    def get_coordinates(self):
        """
        Prompts the client for input coordinates for the desired game character position on the game board.
        If the coordinates are equal to "/q", a message is sent to the server and returns False.
        Else the user input is returned
        :return: User input returned in the form of a string, else return False
        """

        coordinates = input()
        if coordinates == "/q":
            self.send_message(coordinates)
            return False
        return coordinates

    def check_valid_move(self, coordinates, player):
        """
        Tests the received coordinates for validity. Attempts to split coordinates, x and y coordinates
        are checked if they fall in range of the game board, and game board is checked to see if the coordinates
        correspond to an open position. If True, game board is updated with player's character. Else method returns
        False.
        :param coordinates: Represents the desired coordinates on the game board by the player.
        :param player:  Represents the character to be placed
        :return: If coordinates are valid, returns True. Else, Returns False
        """

        # attempts to split user input at "," if error thrown, returns False
        try:
            coord_split = coordinates.split(",")
            int(coord_split[0])
            int(coord_split[1])
        except ValueError:
            return False
        except IndexError:
            return False

        else:
            # splits "coordinates" variable into two variables
            coord_split = coordinates.split(",")
            x_coord = int(coord_split[0])
            y_coord = int(coord_split[1])
            if x_coord <= 2 and y_coord <= 2:                   # checks if x,y coordinates are in range
                if self.game_board[x_coord][y_coord] == "-":     # checks if game board spot is occupied
                    self.game_board[x_coord][y_coord] = player
                    return True

        return False

    def place_char(self, coordinates, player):
        """
        Splits user input into x,y coordinates and places the player's character at the desired coordinates on the
        game board.
        :param coordinates: Represents the input coordinates from a player
        :param player:  Represents a player character
        :return: NONE
        """

        coord_split = coordinates.split(",")
        x_coord = int(coord_split[0])
        y_coord = int(coord_split[1])
        self.game_board[x_coord][y_coord] = player

    def win_check(self, board, player):
        """
        Checks if a user has won the game by placing three of their characters in a row on the game board.
        Checks are made for each row, column and diagonal of the current game board.
        If the variable "char_count" is equal to 3, the player has won the game.
        :param board: Represents the current game board
        :param player: Represents the player's character
        :return: If variable "char_count" is equal to 3, returns True. Else, returns False
        """

        char_count = 0      # variable to track player character counts from the current game board
        # checks each row
        for i in range(3):
            for j in range(3):
                if board[i][j] == player:
                    char_count += 1
            if char_count == 3:
                return True
            char_count = 0

        # checks each column
        for i in range(3):
            for j in range(3):
                if board[j][i] == player:
                    char_count += 1
            if char_count == 3:
                return True
            char_count = 0

        # checks diagonal top-left to bottom-right
        for i in range(3):
            if board[i][i] == player:
                char_count += 1
        if char_count == 3:
            return True
        char_count = 0

        # check diagonal bottom-left to top-right
        for i in range(2, -1):
            if board[i][i] == player:
                char_count += 1
        if char_count == 3:
            return True

        return False

    def initiate_game(self):
        """
        Sends out an initial request to the server. Initial request either invites the server to play tic-tac-toe, or
        prompts server to close its current socket
        :return: If client message is "?", returns True. If client message is "/q", returns False
        """

        while True:
            print("Type '/q' to rage quit at any time")
            print("See if the server would like to play a game of Tic-Tac-Toe by sending '?'")
            snd_message = input()

            # client initiates the game
            if snd_message == "?":
                self.send_message(snd_message)
                return True

            # client closes socket
            elif snd_message == "/q":
                self.send_message(snd_message)
                return False

    def game_accepted(self):
        """
        Checks the client's received message from the server. If the message data is equal to "y", the server has
        accepted the game invitation. If the message data is equal to "/q" or "n", the server has closed its socket.
        :return: True if game invitation was accepted, False otherwise
        """

        # loop to repeatedly check for received message from server
        while True:
            recv_message = self.check_receive()
            if recv_message:

                # Server has closed its socket
                if recv_message == "/q" or recv_message == "n":
                    return False

                # server has accepted game invitation
                if recv_message == "y":
                    return True

    def play_game(self):
        """
        Handles game play for the life of the current game. Calls additional methods for checking and sending data
        between the server, checking validity of moves, checking if the game has been won, and updating the game
        board.
        :return: Returns True if a game is in progress, False if the server's socket is closed
        """

        print("Server has accepted the game!")
        print("You will go first. Enter the row number, followed by a comma, followed by the column number"
              " to pick a spot (e.g.: 0,2)")
        first_move = True
        # loop runs until client or server close their socket
        while True:

            # checks message received by the server
            if not first_move:
                recv_message = self.check_receive()

                # server has closed its socket
                if recv_message == "/q":
                    return False
                self.place_char(recv_message, "O")

                # check if server has won the game
                if self.win_check(self.game_board, "O"):
                    winner = "Server"
                    return self.declare_winner(winner)

            first_move = False
            self.print_board()
            print("Your turn")

            # runs until client enters a valid input or client has won the game
            while True:
                coordinates = self.get_coordinates()

                # checks if client wishes to close their socket
                if not coordinates:
                    return False

                # checks if client input is valid and if client has won the game
                if self.check_valid_move(coordinates, "X"):
                    if self.win_check(self.game_board, "X"):
                        winner = "Client"
                        self.send_message(coordinates)
                        return self.declare_winner(winner)

                    # client entered valid input, game still in progress
                    self.send_message(coordinates)
                    self.round_count += 2
                    if self.round_count == 10:      # checks if we have reached a tie game
                        return self.declare_winner("TIE")
                    break

                # client input is not valid
                else:
                    print("No dice. Please enter a valid move")

    def declare_winner(self, winner):
        """
        Prints to command prompt/terminal at statement declaring the winner or if the game was a tie.
        Sends a message to the server asking if they would like to play again.
        :param winner: represents the winner of the current game
        :return: True if user wishes to play again, False if they have closed their socket
        """
        self.print_board()
        if winner == "TIE":
            print("Tie Game!")
        else:
            print(winner + " has won the game!")

        print("Rematch request sent. Waiting on server response...")
        if winner == "Server":
            snd_message = "Play Again? (y or n)"
            self.send_message(snd_message)

        # loop runs until client receives a message from the server
        while True:
            recv_message = self.check_receive()
            if recv_message:
                if recv_message != "y":
                    return False
                break

        # reset the game board and counters
        self.game_board = []
        self.create_board()
        self.round_count = 0
        return True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    """
    Creates a client side socket and assigns the socket a host and port number and Establishes a connection to the 
    server. Calls methods from the "TicTacToe" class
    """
    game = TicTacToe()
    replay = False
    host = "127.0.0.1"      # host address
    port = 2221             # port number
    client_socket.connect((host, port))      # establishes connection to server, initiates three-way handshake
    print("Connected to local host on port:", port)

    # loop is True until either the server has closed its socket or the client wishes to close its socket
    while True:
        if not replay:
            if not game.initiate_game():    # sends game invitation to server
                break
            if not game.game_accepted():    # receives game invitation response from server
                break
        if not game.play_game():            # begins game play
            break
        replay = True
