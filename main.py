import math
import tkinter as tk
from tkinter import messagebox

import chess


PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

MATE_SCORE = 100000
SEARCH_DEPTH = 2
HUMAN_COLOR = chess.WHITE

LIGHT_SQUARE = "#f0d9b5"
DARK_SQUARE = "#b58863"
SELECTED_SQUARE = "#f6f669"
TARGET_SQUARE = "#cdd26a"
BOARD_BORDER = "#2f2a24"
WINDOW_BG = "#efe7da"
TEXT_COLOR = "#1f2933"
LABEL_FONT = ("Segoe UI", 10, "bold")
PIECE_FONT = ("Segoe UI Symbol", 30)
BOARD_MARGIN = 28
BOARD_PIXELS = 480
SQUARE_SIZE = BOARD_PIXELS // 8

PIECE_SYMBOLS = {
    "P": "\u2659",
    "N": "\u2658",
    "B": "\u2657",
    "R": "\u2656",
    "Q": "\u2655",
    "K": "\u2654",
    "p": "\u265F",
    "n": "\u265E",
    "b": "\u265D",
    "r": "\u265C",
    "q": "\u265B",
    "k": "\u265A",
}

PIECE_SQUARE_TABLES = {
    chess.PAWN: [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -20, -20, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 20, 20, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],
    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50,
    ],
    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ],
    chess.ROOK: [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0,
    ],
    chess.QUEEN: [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -5, 0, 5, 5, 5, 5, 0, -5,
        0, 0, 5, 5, 5, 5, 0, -5,
        -10, 5, 5, 5, 5, 5, 0, -10,
        -10, 0, 5, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20,
    ],
    chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20, 0, 0, 0, 0, 20, 20,
        20, 30, 10, 0, 0, 10, 30, 20,
    ],
}


def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -MATE_SCORE if board.turn == chess.WHITE else MATE_SCORE

    if (
        board.is_stalemate()
        or board.is_insufficient_material()
        or board.can_claim_threefold_repetition()
    ):
        return 0

    score = 0

    for piece_type, value in PIECE_VALUES.items():
        table = PIECE_SQUARE_TABLES[piece_type]

        for square in board.pieces(piece_type, chess.WHITE):
            score += value
            score += table[square]

        for square in board.pieces(piece_type, chess.BLACK):
            score -= value
            score -= table[chess.square_mirror(square)]

    return score


def move_score(board: chess.Board, move: chess.Move) -> int:
    score = 0

    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        moving_piece = board.piece_at(move.from_square)
        captured_value = PIECE_VALUES.get(captured_piece.piece_type, 0) if captured_piece else 0
        moving_value = PIECE_VALUES.get(moving_piece.piece_type, 0) if moving_piece else 0
        score += captured_value - moving_value

    if move.promotion:
        score += PIECE_VALUES.get(move.promotion, 0)

    if board.gives_check(move):
        score += 50

    return score


def ordered_moves(board: chess.Board) -> list[chess.Move]:
    return sorted(board.legal_moves, key=lambda move: move_score(board, move), reverse=True)


def minimax(
    board: chess.Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
) -> tuple[int, chess.Move | None]:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:
        max_eval = -math.inf
        for move in ordered_moves(board):
            board.push(move)
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return int(max_eval), best_move

    min_eval = math.inf
    for move in ordered_moves(board):
        board.push(move)
        eval_score, _ = minimax(board, depth - 1, alpha, beta, True)
        board.pop()

        if eval_score < min_eval:
            min_eval = eval_score
            best_move = move

        beta = min(beta, eval_score)
        if beta <= alpha:
            break

    return int(min_eval), best_move


def get_ai_move(board: chess.Board, depth: int) -> chess.Move | None:
    maximizing_player = board.turn == chess.WHITE
    _, best_move = minimax(board, depth, -math.inf, math.inf, maximizing_player)
    return best_move


def parse_human_move(board: chess.Board, move_text: str) -> chess.Move | None:
    try:
        return board.parse_san(move_text)
    except ValueError:
        pass

    try:
        move = chess.Move.from_uci(move_text)
        if move in board.legal_moves:
            return move
    except ValueError:
        pass

    return None


def game_status_message(board: chess.Board) -> str:
    if board.is_checkmate():
        winner = "Black" if board.turn == chess.WHITE else "White"
        return f"Checkmate. {winner} wins."
    if board.is_stalemate():
        return "Game drawn by stalemate."
    if board.is_insufficient_material():
        return "Game drawn by insufficient material."
    if board.can_claim_threefold_repetition():
        return "Game can be drawn by threefold repetition."
    return f"Game over. Result: {board.result()}"


def piece_symbol(piece: chess.Piece | None) -> str:
    if piece is None:
        return ""
    return PIECE_SYMBOLS[piece.symbol()]


def color_name(color: bool) -> str:
    return "White" if color == chess.WHITE else "Black"


class ChessGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simple Chess Game with Minimax AI")
        self.root.configure(bg=WINDOW_BG)
        self.root.resizable(True, True)

        self.board = chess.Board()
        self.ai_color = not HUMAN_COLOR
        self.selected_square: int | None = None
        self.target_squares: set[int] = set()
        self.thinking = False
        self.board_canvas: tk.Canvas | None = None

        self.status_var = tk.StringVar()
        self.turn_var = tk.StringVar()
        self.last_move_var = tk.StringVar(value="Last move: -")

        self.build_layout()
        self.refresh_board()
        self.set_player_prompt()
        self.fit_window_to_screen()
        self.maybe_start_ai_turn()

    def build_layout(self) -> None:
        outer = tk.Frame(self.root, bg=WINDOW_BG, padx=12, pady=12)
        outer.pack()

        title = tk.Label(
            outer,
            text="Chess vs Minimax AI",
            font=("Segoe UI", 16, "bold"),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            outer,
            text=f"You play as {color_name(HUMAN_COLOR)}.",
            font=("Segoe UI", 10),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        )
        subtitle.pack(anchor="w", pady=(4, 10))

        info_frame = tk.Frame(outer, bg=WINDOW_BG)
        info_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            info_frame,
            textvariable=self.turn_var,
            font=LABEL_FONT,
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
            wraplength=500,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            info_frame,
            textvariable=self.last_move_var,
            font=("Segoe UI", 10),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        ).pack(anchor="w", pady=(4, 0))

        controls = tk.Frame(outer, bg=WINDOW_BG)
        controls.pack(fill="x", pady=(0, 10))

        self.move_entry = tk.Entry(controls, font=("Consolas", 12), width=16)
        self.move_entry.pack(side="left")
        self.move_entry.bind("<Return>", self.submit_typed_move)

        tk.Button(
            controls,
            text="Play Move",
            command=self.submit_typed_move,
            font=("Segoe UI", 10, "bold"),
            bg="#315d80",
            fg="white",
            activebackground="#254963",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="left", padx=(8, 8))

        tk.Button(
            controls,
            text="New Game",
            command=self.reset_game,
            font=("Segoe UI", 10, "bold"),
            bg="#5a7d4f",
            fg="white",
            activebackground="#46623e",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            controls,
            text="Undo Move",
            command=self.undo_last_turn,
            font=("Segoe UI", 10, "bold"),
            bg="#8a5a44",
            fg="white",
            activebackground="#6d4635",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
        ).pack(side="left")

        board_container = tk.Frame(outer, bg=BOARD_BORDER, padx=6, pady=6)
        board_container.pack()

        canvas_size = BOARD_PIXELS + (BOARD_MARGIN * 2)
        self.board_canvas = tk.Canvas(
            board_container,
            width=canvas_size,
            height=canvas_size,
            bg=BOARD_BORDER,
            highlightthickness=0,
            bd=0,
        )
        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.handle_board_click)

    def fit_window_to_screen(self) -> None:
        self.root.update_idletasks()
        requested_width = self.root.winfo_reqwidth()
        requested_height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = min(requested_width, screen_width - 80)
        height = min(requested_height, screen_height - 120)
        x_pos = max((screen_width - width) // 2, 0)
        y_pos = max((screen_height - height) // 2, 0)

        self.root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.root.minsize(width, height)

    def displayed_files(self) -> list[int]:
        if HUMAN_COLOR == chess.WHITE:
            return list(range(8))
        return list(range(7, -1, -1))

    def displayed_ranks(self) -> list[int]:
        if HUMAN_COLOR == chess.WHITE:
            return list(range(7, -1, -1))
        return list(range(8))

    def handle_board_click(self, event: tk.Event) -> None:
        square = self.square_from_canvas(event.x, event.y)
        if square is not None:
            self.on_square_click(square)

    def square_from_canvas(self, x_pos: int, y_pos: int) -> int | None:
        board_left = BOARD_MARGIN
        board_top = BOARD_MARGIN
        board_right = board_left + BOARD_PIXELS
        board_bottom = board_top + BOARD_PIXELS

        if not (board_left <= x_pos < board_right and board_top <= y_pos < board_bottom):
            return None

        file_index = (x_pos - board_left) // SQUARE_SIZE
        rank_index = (y_pos - board_top) // SQUARE_SIZE
        displayed_files = self.displayed_files()
        displayed_ranks = self.displayed_ranks()

        return chess.square(displayed_files[file_index], displayed_ranks[rank_index])

    def on_square_click(self, square: int) -> None:
        if self.thinking:
            self.status_var.set("The AI is thinking. Please wait for its move.")
            return

        if self.board.is_game_over():
            self.status_var.set("The game is finished. Start a new game to play again.")
            return

        if self.board.turn != HUMAN_COLOR:
            self.status_var.set("It is the AI's turn.")
            return

        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece and piece.color == HUMAN_COLOR:
                self.select_square(square)
            else:
                self.status_var.set("Select one of your own pieces to begin a move.")
            return

        if square == self.selected_square:
            self.clear_selection()
            self.set_player_prompt()
            return

        move = self.find_move(self.selected_square, square)
        if move is not None:
            self.play_human_move(move)
            return

        if piece and piece.color == HUMAN_COLOR:
            self.select_square(square)
            return

        self.status_var.set("That is not a legal destination for the selected piece.")

    def select_square(self, square: int) -> None:
        self.selected_square = square
        self.target_squares = {
            move.to_square
            for move in self.board.legal_moves
            if move.from_square == square
        }
        self.refresh_board()
        self.status_var.set(f"Selected {chess.square_name(square)}. Choose a destination square.")

    def clear_selection(self) -> None:
        self.selected_square = None
        self.target_squares.clear()
        self.refresh_board()

    def find_move(self, from_square: int, to_square: int) -> chess.Move | None:
        matching_moves = [
            move
            for move in self.board.legal_moves
            if move.from_square == from_square and move.to_square == to_square
        ]

        if not matching_moves:
            return None

        queen_promotion = next(
            (move for move in matching_moves if move.promotion == chess.QUEEN),
            None,
        )
        return queen_promotion or matching_moves[0]

    def submit_typed_move(self, _event: tk.Event | None = None) -> None:
        if self.thinking:
            self.status_var.set("The AI is thinking. Please wait for its move.")
            return

        if self.board.is_game_over():
            self.status_var.set("The game is finished. Start a new game to play again.")
            return

        if self.board.turn != HUMAN_COLOR:
            self.status_var.set("It is the AI's turn.")
            return

        move_text = self.move_entry.get().strip()
        if not move_text:
            self.status_var.set("Enter a move like e2e4 or Nf3, or click a piece on the board.")
            return

        move = parse_human_move(self.board, move_text)
        if move is None:
            self.status_var.set("Invalid move. Try UCI like e2e4 or SAN like Nf3.")
            return

        self.play_human_move(move)

    def play_human_move(self, move: chess.Move) -> None:
        move_san = self.board.san(move)
        self.board.push(move)
        self.move_entry.delete(0, tk.END)
        self.clear_selection()
        self.last_move_var.set(f"Last move: You played {move_san} ({move.uci()})")
        self.refresh_board()

        if self.board.is_game_over():
            self.finish_game()
            return

        self.thinking = True
        self.status_var.set("AI is thinking...")
        self.turn_var.set(f"Turn: {color_name(self.ai_color)} AI")
        self.root.after(150, self.play_ai_turn)

    def play_ai_turn(self) -> None:
        ai_move = get_ai_move(self.board, SEARCH_DEPTH)
        self.thinking = False

        if ai_move is None:
            self.finish_game()
            return

        move_san = self.board.san(ai_move)
        self.board.push(ai_move)
        self.last_move_var.set(f"Last move: AI played {move_san} ({ai_move.uci()})")
        self.refresh_board()

        if self.board.is_game_over():
            self.finish_game()
            return

        self.set_player_prompt()

    def finish_game(self) -> None:
        self.clear_selection()
        message = game_status_message(self.board)
        self.status_var.set(message)
        self.turn_var.set(f"Final result: {self.board.result()}")
        messagebox.showinfo("Game Over", f"{message}\nResult: {self.board.result()}")

    def undo_last_turn(self) -> None:
        if self.thinking:
            self.status_var.set("Wait for the AI move to finish before undoing.")
            return

        moves_to_undo = 2 if self.board.turn == HUMAN_COLOR and len(self.board.move_stack) >= 2 else 1
        if len(self.board.move_stack) < moves_to_undo:
            self.status_var.set("No move to undo yet.")
            return

        for _ in range(moves_to_undo):
            self.board.pop()

        self.selected_square = None
        self.target_squares.clear()
        self.move_entry.delete(0, tk.END)
        self.last_move_var.set("Last move: -")
        self.refresh_board()
        self.set_player_prompt()

    def reset_game(self) -> None:
        self.board.reset()
        self.selected_square = None
        self.target_squares.clear()
        self.thinking = False
        self.last_move_var.set("Last move: -")
        self.move_entry.delete(0, tk.END)
        self.refresh_board()
        self.set_player_prompt()
        self.maybe_start_ai_turn()

    def set_player_prompt(self) -> None:
        self.turn_var.set(f"Turn: {color_name(HUMAN_COLOR)} (You)")
        self.status_var.set(
            "Your move. Click a piece and a destination square, or type a move. Promotions default to a queen."
        )

    def maybe_start_ai_turn(self) -> None:
        if self.board.turn != self.ai_color or self.board.is_game_over():
            return

        self.thinking = True
        self.turn_var.set(f"Turn: {color_name(self.ai_color)} AI")
        self.status_var.set(f"{color_name(self.ai_color)} AI is thinking...")
        self.root.after(150, self.play_ai_turn)

    def refresh_board(self) -> None:
        if self.board_canvas is None:
            return

        self.board_canvas.delete("all")
        displayed_files = self.displayed_files()
        displayed_ranks = self.displayed_ranks()
        board_left = BOARD_MARGIN
        board_top = BOARD_MARGIN
        board_right = board_left + BOARD_PIXELS
        board_bottom = board_top + BOARD_PIXELS

        self.board_canvas.create_rectangle(
            board_left,
            board_top,
            board_right,
            board_bottom,
            outline=BOARD_BORDER,
            width=2,
        )

        for index, file_index in enumerate(displayed_files):
            x_pos = board_left + (index * SQUARE_SIZE) + (SQUARE_SIZE / 2)
            self.board_canvas.create_text(
                x_pos,
                board_bottom + (BOARD_MARGIN / 2),
                text=chess.FILE_NAMES[file_index],
                fill="white",
                font=LABEL_FONT,
            )

        for index, rank_index in enumerate(displayed_ranks):
            y_pos = board_top + (index * SQUARE_SIZE) + (SQUARE_SIZE / 2)
            self.board_canvas.create_text(
                BOARD_MARGIN / 2,
                y_pos,
                text=str(rank_index + 1),
                fill="white",
                font=LABEL_FONT,
            )

        for row_index, rank_index in enumerate(displayed_ranks):
            for col_index, file_index in enumerate(displayed_files):
                square = chess.square(file_index, rank_index)
                x1 = board_left + (col_index * SQUARE_SIZE)
                y1 = board_top + (row_index * SQUARE_SIZE)
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                self.board_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=self.square_color(square),
                    outline="",
                )

                piece = self.board.piece_at(square)
                if piece is not None:
                    self.board_canvas.create_text(
                        x1 + (SQUARE_SIZE / 2),
                        y1 + (SQUARE_SIZE / 2),
                        text=piece_symbol(piece),
                        fill=TEXT_COLOR,
                        font=PIECE_FONT,
                    )

    def square_color(self, square: int) -> str:
        if square == self.selected_square:
            return SELECTED_SQUARE
        if square in self.target_squares:
            return TARGET_SQUARE
        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)
        return LIGHT_SQUARE if (file_index + rank_index) % 2 == 0 else DARK_SQUARE


def main() -> None:
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
