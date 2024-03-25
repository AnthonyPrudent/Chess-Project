# Author: Anthony Prudent
# GitHub username: AnthonyPrudent
# Date: 3/6/2024
# Description: The program defines two classes to represent chess pieces as well as a variation of a game of chess.
#              the chess piece class initializes with a specified piece type and player color. The chess piece private
#              data members such as max moves, move set, and symbol are modified depending on the specified piece type.
#              The chess game class initializes the board, game state, and tracking private data members. The make move
#              method uses recursion to move through the spaces required to reach the destination with base cases to
#              prevent illegal moves or to handle special cases. Both classes feature get methods to access certain
#              private data members.


class ChessPiece:
    """
    Represents a chess piece. Stores the information about the chess piece such as the type, available move set, player
    color, maximum moves that can be made, symbol representation. Communicates with the ChessVar class to initialize
    and update the chess board and access necessary information to validate moves.
    """

    def __init__(self, piece_type, player_color):
        """
        Initializes the chess piece object with the specified type and player color. Additional private data members
        are initialized and changed depending on the type of the chess piece such as max moves, move set, and symbol.
        """
        self._piece_type = piece_type
        self._player_color = player_color
        self._max_moves = 7
        self._symbol = self._player_color[0].upper() + self._piece_type[0].upper()
        self._move_set = None

        if self._piece_type == "pawn":
            self._max_moves = 2

            if self._player_color == "white":
                self._move_set = ["vertical_up"]

            else:
                self._move_set = ["vertical_down"]

        if self._piece_type == "knight":
            self._max_moves = 3
            self._symbol = self._player_color[0].upper() + self._piece_type[0]
            self._move_set = ["horizontal", "vertical_up", "vertical_down"]

        if self._piece_type == "king":
            self._max_moves = 1
            self._move_set = ["diagonal", "horizontal", "vertical_up", "vertical_down"]

        if self._piece_type == "queen":
            self._move_set = ["diagonal", "horizontal", "vertical_up", "vertical_down"]

        if self._piece_type == "rook":
            self._move_set = ["horizontal", "vertical_up", "vertical_down"]

        if self._piece_type == "bishop":
            self._move_set = ["diagonal"]

        if self._piece_type == "falcon":

            if self._player_color == "white":
                self._move_set = ["diagonal_up", "vertical_down"]

            else:
                self._move_set = ["diagonal_down", "vertical_up"]

        if self._piece_type == "hunter":

            if self._player_color == "white":
                self._move_set = ["vertical_up", "diagonal_down"]

            else:
                self._move_set = ["vertical_down", "diagonal_up"]

    def get_max_moves(self):
        """
        Return the max moves that the chess piece can make.
        Used to limit similarly moving chess pieces depending on type.
        """
        return self._max_moves

    def set_max_moves(self, amount):
        """
        Sets the max amount moves that a chess piece can make. Used to decrease max pawn move after first.
        """
        self._max_moves = amount

    def get_player_color(self):
        """
        Returns the player color of the chess piece.
        Used to check if the chess piece can be captured or blocking friendly chess piece.
        """
        return self._player_color

    def get_piece_type(self):
        """
        Returns the type of the chess piece.
        Used to check if special cases must be considered when moving chess piece.
        """
        return self._piece_type

    def get_symbol(self):
        """
        Returns the string representation of the chess.
        Used to represent the type and color of a chess piece as a string.
        """
        return self._symbol

    def get_move_set(self):
        """
        Returns the move set list of the chess piece. Used to determine which types of moves that the chess piece can
        make.
        """
        return self._move_set


class ChessVar:
    """
    Represents a variation of a game of chess. Creates the chess board and keeps track of player turn, board columns
    and rows, game state, special chess pieces, and chess pieces on the board. Communicates with the
    ChessPiece class to move chess pieces on the board.
    """

    def __init__(self):
        """
        Initializes the chess game variation. Initializes information about the chess game such as game state,
        player turn, chess board locations and status, and deployment of special pawns.
        """

        self._game_state = "UNFINISHED"
        self._player_color_turn = "white"
        self._chess_board = {}
        self._rows = ("1", "2", "3", "4", "5", "6", "7", "8")
        self._columns = ("a", "b", "c", "d", "e", "f", "g", "h")
        self._home_pieces_order = ("rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook")
        self._fairy_pieces_played = {"white": [], "black": []}
        self._play_fairy_check = {
            "black": {"queen": 1, "rook": 2, "bishop": 2, "knight": 2},
            "white": {"queen": 1, "rook": 2, "bishop": 2, "knight": 2}
        }

        # Initialize all locations of the chess board
        for row in self._rows:
            for column in self._columns:
                square_location = column + row
                self._chess_board[square_location] = None

        # Initialize pawns for both players
        for column in self._columns:
            self._chess_board[column + "2"] = ChessPiece("pawn", "white")
            self._chess_board[column + "7"] = ChessPiece("pawn", "black")

        # Initialize non-pawn pieces
        for index in range(len(self._columns)):
            column = self._columns[index]
            non_pawn = self._home_pieces_order[index]
            self._chess_board[column + "1"] = ChessPiece(non_pawn, "white")
            self._chess_board[column + "8"] = ChessPiece(non_pawn, "black")

        print(self.get_chess_board_display())

    def get_game_state(self):
        """
        Return the state of the chess game.
        """
        return self._game_state

    def make_move(self, current_space, destination_space, move_counter=0, original_space=None):
        """
        Recursively Moves the chess piece located at the current space to the destination space if legal, returning
        a Boolean value depending on the success of the move. In each recursive call, current space is used to move the
        chess piece towards the defined destination space. Move counter is used to track the number of moves and compare
        to the max amount of moves a piece can make. Original space is used to access the original location and
        chess piece object.
        """

        # Base case if the specified spaces are invalid
        if current_space not in self._chess_board or destination_space not in self._chess_board:
            return False

        # Saves the original starting space location
        if original_space is None:
            original_space = current_space

        original_space_piece = self._chess_board[original_space]

        #  Base case if there is a piece to be moved at all
        if original_space_piece is None:
            return False

        #  Base case if the game is over
        if self._game_state != "UNFINISHED":
            return False

        original_piece_color = original_space_piece.get_player_color()

        #  Base case if the piece to be moved is the same color as the player
        if original_piece_color != self._player_color_turn:
            return False

        move_set = original_space_piece.get_move_set()

        current_column = current_space[0]
        current_row = current_space[1]

        current_column_index = self._columns.index(current_column)
        current_row_index = self._rows.index(current_row)

        destination_column = destination_space[0]
        destination_row = destination_space[1]

        current_space_piece = self._chess_board[current_space]
        destination_space_piece = self._chess_board[destination_space]

        column_diff = self._columns.index(destination_column) - self._columns.index(current_column)
        row_diff = self._rows.index(destination_row) - self._rows.index(current_row)

        original_piece_type = original_space_piece.get_piece_type()

        diagonal_slope = None

        if row_diff != 0 and column_diff != 0:
            diagonal_slope = row_diff / column_diff

        # Knight cannot move in a straight line or diagonally within its range
        if original_piece_type == "knight" and move_counter == 0:

            if column_diff == 0 or row_diff == 0:
                return False

            if column_diff % 2 != 0 and row_diff % 2 != 0:
                return False

        # Special cases for when there is a chess piece at the destination space
        if destination_space_piece is not None:

            destination_piece_color = destination_space_piece.get_player_color()

            #  Base case if one of the player's piece is blocking the destination
            if destination_piece_color == self._player_color_turn:
                return False

            # Allows pawn to move diagonally if there is an immediate opponent piece
            if original_piece_type == "pawn" and move_counter == 0:

                if column_diff != 0 and row_diff != 0:

                    if 1 % column_diff == 0 and 1 % row_diff == 0:

                        if original_space_piece.get_player_color() == "white":
                            original_space_piece.get_move_set().append("diagonal_up")

                        else:
                            original_space_piece.get_move_set().append("diagonal_down")

        # Base case if there is a piece obstructing the path unless the moving piece is a knight
        if current_space_piece is not None and move_counter > 0 and current_space != destination_space:

            if original_piece_type != "knight":
                return False

        # Base case if the destination space is out of the range of the moving piece
        if move_counter > original_space_piece.get_max_moves():
            return False

        # Base case if the move is able to be made
        if current_space == destination_space:

            # If there is a chess piece at the destination space
            if destination_space_piece is not None:

                destination_piece_type = destination_space_piece.get_piece_type()

                # Captured destination piece is the King and game over
                if destination_piece_type == "king":
                    self._game_state = original_piece_color.upper() + "_WON"
                    print(self.get_game_state())

                # Pawn cannot capture a piece vertically
                if original_piece_type == "pawn":

                    if "diagonal_down" not in move_set and "diagonal_up" not in move_set:
                        return False

                pieces_to_check = self._play_fairy_check[destination_space_piece.get_player_color()]

                # Decrements the special pawn count for fairy pieces
                if destination_piece_type in pieces_to_check:
                    pieces_to_check[destination_piece_type] -= 1

            # Special cases after a pawn moves
            if original_piece_type == "pawn":

                # Pawns only move one space after first move
                original_space_piece.set_max_moves(1)

                # Remove the pawn's special diagonal move after capturing opponent pawn
                if "diagonal_up" in move_set:
                    original_space_piece.get_move_set().remove("diagonal_up")

                if "diagonal_down" in move_set:
                    original_space_piece.get_move_set().remove("diagonal_down")

            self._chess_board[destination_space] = original_space_piece
            self._chess_board[original_space] = None

            # Changes the whose turn it is
            if self._player_color_turn == "white":
                self._player_color_turn = "black"
            else:
                self._player_color_turn = "white"

            print(self.get_chess_board_display())
            return True

        # Move diagonally
        if "diagonal_up" in move_set or "diagonal" in move_set:

            # Move upper-right
            if row_diff > 0 and column_diff > 0 and diagonal_slope == 1:
                current_space = self._columns[current_column_index + 1] + self._rows[current_row_index + 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

            # Move diagonally upper-left
            if row_diff > 0 > column_diff and diagonal_slope == -1:
                current_space = self._columns[current_column_index - 1] + self._rows[current_row_index + 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

        if "diagonal_down" in move_set or "diagonal" in move_set:

            # Move diagonally lower-right
            if row_diff < 0 < column_diff and diagonal_slope == -1:
                current_space = self._columns[current_column_index + 1] + self._rows[current_row_index - 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

            # Move diagonally lower-left
            if row_diff < 0 and column_diff < 0 and diagonal_slope == 1:
                current_space = self._columns[current_column_index - 1] + self._rows[current_row_index - 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

        # Move horizontally
        if "horizontal" in move_set and row_diff == 0 or original_piece_type == "knight":

            # Move right
            if column_diff >= 1:
                current_space = self._columns[current_column_index + 1] + current_row
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

            # Move left
            if column_diff <= -1:
                current_space = self._columns[current_column_index - 1] + current_row
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

        # Move up
        if "vertical_up" in move_set and column_diff == 0 or original_piece_type == "knight":

            if row_diff >= 1:
                current_space = self._columns[current_column_index] + self._rows[current_row_index + 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

        # Move down
        if "vertical_down" in move_set and column_diff == 0 or original_piece_type == "knight":

            if row_diff <= -1:
                current_space = self._columns[current_column_index] + self._rows[current_row_index - 1]
                return self.make_move(current_space, destination_space, move_counter + 1, original_space)

        # The chess piece is unable to move to the destination
        return False

    def enter_fairy_piece(self, piece_type, enter_square):
        """
        Initializes the fairy piece in the specified location if legal, returning Boolean value depending on
        successful initialization. The piece type is used to deduce the fairy piece's color and type while the enter
        square is used to determine the starting location in either player's two home ranks.
        """
        home_rank_rows = ("1", "2", "7", "8")

        # Checks if the piece_type length is valid
        if len(piece_type) > 1 or piece_type == "":
            return False

        # Checks if the game is unfinished
        if self._game_state != "UNFINISHED":
            return False

        # Checks if the fairy piece is entering on a valid, empty space
        if enter_square not in self._chess_board or self._chess_board[enter_square] is not None:
            return False

        # The fairy piece is not entering a home rank space
        if enter_square[1] not in home_rank_rows:
            return False

        # piece type matches the player color of the current turn
        if piece_type.isupper() and self._player_color_turn == "black":
            return False

        if piece_type.islower() and self._player_color_turn == "white":
            return False

        fairy_pieces_played = self._fairy_pieces_played[self._player_color_turn]

        # Manipulate piece type from user input
        fairy_piece_type = piece_type.lower()

        if fairy_piece_type == "f":
            fairy_piece_type = "falcon"

        if fairy_piece_type == "h":
            fairy_piece_type = "hunter"

        # Checks if the fairy piece is played
        if fairy_piece_type not in fairy_pieces_played:

            total_pieces = 0
            first_fairy_piece_check = 6
            second_fairy_piece_check = 5
            pieces_to_check = self._play_fairy_check[self._player_color_turn]
            fairy_piece = None

            # Counts the number of special pieces of the player's turn
            for piece_type in pieces_to_check:
                total_pieces += pieces_to_check[piece_type]

            # The first fairy piece can be played after losing a special piece
            if len(fairy_pieces_played) == 0 and total_pieces <= first_fairy_piece_check:
                fairy_piece = ChessPiece(fairy_piece_type, self._player_color_turn)

            # The second fairy piece can be played after losing another special piece
            if len(fairy_pieces_played) == 1 and total_pieces <= second_fairy_piece_check:
                fairy_piece = ChessPiece(fairy_piece_type, self._player_color_turn)

            # Enter the fairy piece on the given space
            if fairy_piece is not None:

                # The fairy piece starts on the white home ranks
                if enter_square[1] == "1" or enter_square[1] == "2" and self._player_color_turn == "white":
                    self._chess_board[enter_square] = fairy_piece

                # The fairy piece starts on the black home ranks
                if enter_square[1] == "8" or enter_square[1] == "7" and self._player_color_turn == "black":
                    self._chess_board[enter_square] = fairy_piece

                fairy_pieces_played.append(fairy_piece_type)

                # Changes the whose turn it is
                if self._player_color_turn == "white":
                    self._player_color_turn = "black"
                else:
                    self._player_color_turn = "white"

                print(self.get_chess_board_display())

                return True

            # The player must lose more special pieces to enter a fairy piece
            return False

        # The fairy piece is already in play
        return False

    def get_chess_board_display(self):
        """
        Creates and returns the string representation of the current chess board.
        """
        chess_board = []

        for row in self._rows:

            temporary_line = []

            for column in self._columns:
                square_location = column + row
                temporary_line.append(square_location)

            chess_board.append(temporary_line)

        chess_board_string = "   a   b   c   d   e   f   g   h\n"
        empty_square = "[  ]"

        for line_index in range(len(chess_board) - 1, -1, -1):

            chess_board_string = chess_board_string + str(line_index + 1) + " "

            for square_location_index in range(0, len(chess_board[line_index])):

                square_location = chess_board[line_index][square_location_index]

                if self._chess_board[square_location] is not None:
                    piece_symbol = self._chess_board[square_location].get_symbol()
                    chess_board_string = chess_board_string + "[" + piece_symbol + "]"

                else:
                    chess_board_string = chess_board_string + empty_square

                if square_location_index == 7:
                    chess_board_string = chess_board_string + "\n"

        return chess_board_string
