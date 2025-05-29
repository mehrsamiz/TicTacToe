import time
from math import inf as infinity

class TicTacToe:
    def __init__(self):
        # Initialize empty board and no winner
        self.board = [' ' for _ in range(9)]
        self.winner = None

    def display_board(self):
        """Display the current game board with clearer formatting."""
        board_display = [str(i + 1) if cell == ' ' else cell for i, cell in enumerate(self.board)]
        print("\nCurrent Board:")
        print(f" {board_display[0]} | {board_display[1]} | {board_display[2]} ")
        print("---+---+---")
        print(f" {board_display[3]} | {board_display[4]} | {board_display[5]} ")
        print("---+---+---")
        print(f" {board_display[6]} | {board_display[7]} | {board_display[8]} \n")

    def win_check(self):
        """Check all win conditions and set the winner if found."""
        win_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for i, j, k in win_positions:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                self.winner = self.board[i]
                return True
        return False

    def endgame(self):
        """Return True if the game is over (win or tie)."""
        return self.win_check() or ' ' not in self.board

    def free_pos(self):
        """Return a list of available positions on the board."""
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def make_move(self, position, player_label):
        """Attempt to make a move at the given position."""
        if self.board[position] == ' ':
            self.board[position] = player_label
            return True
        return False

    def minimax(self, depth, is_maximizing, player_label, opponent_label):
        """
        Minimax algorithm: explore all possible moves and choose the optimal one.
        """
        if depth == 0 or self.endgame():
            return -1, self.evaluate(player_label)

        best_score = -infinity if is_maximizing else infinity
        best_move = -1

        for move in self.free_pos():
            self.board[move] = player_label if is_maximizing else opponent_label
            _, score = self.minimax(depth - 1, not is_maximizing, player_label, opponent_label)
            self.board[move] = ' '  # undo move

            if is_maximizing and score > best_score:
                best_score, best_move = score, move
            elif not is_maximizing and score < best_score:
                best_score, best_move = score, move

        return best_move, best_score

    def evaluate(self, player_label):
        """Evaluate the board score from the AI's perspective."""
        if self.winner == player_label:
            return 1
        elif self.winner is None and ' ' not in self.board:
            return 0  # draw
        return -1  # opponent wins


class Player:
    def __init__(self, label, ai=False):
        self.label = label
        self.ai = ai

    def take_turn(self, game):
        """Take a turn: AI uses minimax, human enters input."""
        if self.ai:
            print("AI's Turn:")
            move, _ = game.minimax(
                depth=len(game.free_pos()),
                is_maximizing=True,
                player_label=self.label,
                opponent_label='X' if self.label == 'O' else 'O'
            )
            game.make_move(move, self.label)
        else:
            print("Your Turn:")
            while True:
                try:
                    move = int(input("Enter position (1-9): ")) - 1
                    if move in game.free_pos():
                        game.make_move(move, self.label)
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Enter a valid number between 1 and 9.")


if __name__ == "__main__":
    game = TicTacToe()

    # Let human choose their symbol
    h_label = ''
    while h_label not in ['X', 'O']:
        h_label = input("Choose X or O:\n").upper()

    human_player = Player(label=h_label)
    ai_player = Player(label='O' if h_label == 'X' else 'X', ai=True)

    # Game begins
    game.display_board()
    while not game.endgame():
        human_player.take_turn(game)
        game.display_board()
        if game.endgame():
            break
        ai_player.take_turn(game)
        time.sleep(0.5)
        game.display_board()

    # Game ends
    if game.winner:
        print(f"🏁 Winner is: {game.winner}")
    else:
        print("🤝 It's a tie!")
