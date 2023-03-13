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
    def __init__(self):
        """
        Creates a TicTacToe Object. This class is responsible for initializing and creating a tic-tac-toe game board
        and tracking how many rounds have been played throughout the course of the game. Includes various methods for
        carryingout game play.
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
        Checks if the server has received a response from the client. Received messages are decoded and returned.
        :return: Decoded message as a string
        """

        recv_message = conn_socket.recv(2221)
        decoded_message = recv_message.decode()
        return decoded_message

    def send_message(self, message):
        """
        Receives a server created message. The message is encoded and sent to the client
        :param message: Represents the message created by the server
        :return: NONE
        """

        encoded_message = message.encode()
        conn_socket.send(encoded_message)

    def get_coordinates(self):
        """
        Prompts the server for input coordinates for the desired game character position on the game board.
        If the coordinates are equal to "/q", a message is sent to the client and returns False.
        Else the user input is returned.
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
            if x_coord <= 2 and y_coord <= 2:
                if self.game_board[x_coord][y_coord] == "-":        # checks if x,y coordinates are in range
                    self.game_board[x_coord][y_coord] = player      # checks if game board spot is occupied
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

        # check diagonal right to left
        for i in range(2, -1):
            if board[i][i] == player:
                char_count += 1
        if char_count == 3:
            return True

        return False

    def initiate_game(self):
        """
        Receives a request from the client. Initial request either invites the server to play tic-tac-toe, or
        prompts server to close its current socket. Server responds by either accepting or denying game invitation.
        :return: If client message is "?" and server response is "y", returns True.
                 If client message is "/q" or server response is "/q" or "n", returns False
        """

        decoded_message = self.check_receive()
        # client sent game invitation
        if decoded_message == "?":
            print(decoded_message)
            print("Type '/q' to rage quit at any time")

            # loops until server gives valid response
            while True:
                print("Type 'y' to play or 'n' to decline")
                snd_message = input()

                # server accepts game invitation
                if snd_message == "y":
                    self.send_message(snd_message)
                    return True

                # server denies game invitation
                elif snd_message == "n" or snd_message == "/q":
                    self.send_message(snd_message)
                    break

        return False

    def play_game(self):
        """
        Handles game play for the life of the current game. Calls additional methods for checking and sending data
        between the server, checking validity of moves, checking if the game has been won, and updating the game
        board.
        :return: Returns True if a game is in progress, False if the client's socket is closed
        """

        print("You will be 'Os'. Enter the row number, followed by a comma, followed by the column number"
              " to pick a spot (e.g.: 0,2)")

        # loop runs until client or server close their socket
        while True:
            recv_message = self.check_receive()
            # checks message received by the client
            if recv_message:

                # client has closed its socket
                if recv_message == "/q":
                    return False
                self.place_char(recv_message, "X")

                # check if client has won the game
                if self.win_check(self.game_board, "X"):
                    winner = "Client"
                    return self.declare_winner(winner)

                self.round_count += 2
                if self.round_count > 9:        # checks if we have reached a tie game
                    return self.declare_winner("TIE")
                self.print_board()
                print("Your turn")

                # runs until server enters a valid input or server has won the game
                while True:
                    coordinates = self.get_coordinates()

                    # checks if server wishes to close their socket
                    if not coordinates:
                        return False

                    # checks if server input is valid and if server has won the game
                    if self.check_valid_move(coordinates, "O"):
                        if self.win_check(self.game_board, "O"):
                            winner = "Server"
                            self.send_message(coordinates)
                            return self.declare_winner(winner)

                        # server input was valid, game still in progress
                        self.send_message(coordinates)
                        break

                    # server input is not valid
                    else:
                        print("No dice. Please enter a valid move")

    def declare_winner(self, winner):
        """
        Prints to command prompt/terminal at statement declaring the winner or if the game was a tie.
        Invites the server to play again
        :param winner: represents the winner of the current game
        :return: True if server wishes to play again, False if invitation was declined
        """

        self.print_board()
        if winner == "TIE":
            print("Tie Game!")
        else:
            print(winner + " has won the game")

        if winner == "Server":
            recv_message = self.check_receive()
            print(recv_message)

        # loops until server enters a valid response
        while True:
            print("Type 'y' to play again or 'n' to quit")
            snd_message = input()
            if snd_message == "y":
                play_again = True
                break
            if snd_message == "n":
                play_again = False
                break

        # send message to client and reset the game board and counters
        self.send_message(snd_message)
        self.game_board = []
        self.create_board()
        self.round_count = 0
        return play_again


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receiver_socket:
    """
    Creates a server side socket and assigns an IP address and port number to the server socket. The socket then
    begins listening for incoming connections. Once a connection is made, the server accepts the request from the 
    client. Calls methods from the "TicTacToe" class.
    """

    game = TicTacToe()
    replay = False
    host = "127.0.0.1"  # host address
    port = 2221  # port number
    receiver_socket.bind((host, port))  # binds the socket to the address
    receiver_socket.listen(1)  # enables server to accept connections
    print("Waiting for message...")

    # accepts a connection, conn_socket = new socket object used to send and receive data on the connection
    # addr = address bound to socket on other end of connection
    conn_socket, addr = receiver_socket.accept()
    print("Server listening on: localhost on port:", port, "\n" "Connected by:", host, addr)

    # loop is True until either the client has closed its socket or the server wishes to close its socket
    while True:
        if not replay:
            if not game.initiate_game():    # accepts or denies game invitation from client
                break
        if not game.play_game():            # begins game play
            break
        replay = True
