import tkinter as tk

from game import GameState
from ai import AI

BG = "#1f4d36"
LIVE_BG = "white"
LIVE_FG = "black"
SELECTED_BG = "#1f4d36"
SELECTED_FG = "white"
DEAD_BG = "#1f4d36"
DEAD_FG = "#5f9179"
DEAD_BORDER = "#5f9179"
LINK_FG = "#a9cbb9"
NAV_BG = "#123320"
NAV_BG_HOVER = "#1a4a2e"
NAV_FG = "white"

DIFFICULTY_NAMES = {
    1: "Easy",
    2: "Medium",
    3: "Hard",
}

class SticksGUI:

    def __init__(self, root, difficulty):
        self.root = root
        self.game = GameState()
        self.ai = AI(side="ai", depth=difficulty)
        self.difficulty = difficulty

        self.selected_hand = None
        self.ai_thinking = False

        self.root.title("Sticks")
        self.root.geometry("700x700")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.top_bar = tk.Frame(
            root,
            bg=BG
        )
        self.top_bar.pack(
            fill="x",
            padx=20,
            pady=(16, 0)
        )

        self.quit_button = tk.Button(
            self.top_bar,
            text="Quit",
            font=("Times New Roman", 14),
            fg=NAV_FG,
            bg=NAV_BG,
            activeforeground=NAV_FG,
            activebackground=NAV_BG_HOVER,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=14,
            pady=6,
            command=self.quit_game
        )
        self.quit_button.pack(
            side="right"
        )

        self.menu_button = tk.Button(
            self.top_bar,
            text="Menu",
            font=("Times New Roman", 14),
            fg=NAV_FG,
            bg=NAV_BG,
            activeforeground=NAV_FG,
            activebackground=NAV_BG_HOVER,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=14,
            pady=6,
            command=self.go_to_menu
        )
        self.menu_button.pack(
            side="right",
            padx=(0, 14)
        )

        self.title_label = tk.Label(
            root,
            text="Sticks",
            font=("Times New Roman", 30, "bold"),
            fg="white",
            bg=BG
        )
        self.title_label.pack(
            pady=(10, 2)
        )

        self.difficulty_label = tk.Label(
            root,
            text=f"Difficulty: {DIFFICULTY_NAMES.get(difficulty, '')}",
            font=("Times New Roman", 15, "bold"),
            fg=LINK_FG,
            bg=BG
        )
        self.difficulty_label.pack(
            pady=(0, 5)
        )

        self.moves_label = tk.Label(
            root,
            text="Moves remaining: 100",
            font=("Times New Roman", 14, "bold"),
            fg=LINK_FG,
            bg=BG
        )
        self.moves_label.pack(
            pady=(0, 14)
        )

        self.turn_label = tk.Label(
            root,
            text="",
            font=("Times New Roman", 17, "bold"),
            fg="white",
            bg=BG
        )
        self.turn_label.pack(
            pady=(0, 28)
        )

        self.ai_label = tk.Label(
            root,
            text="AI",
            font=("Times New Roman", 17, "bold"),
            fg="white",
            bg=BG
        )
        self.ai_label.pack(
            pady=(0, 12)
        )

        self.ai_hands_frame = tk.Frame(
            root,
            bg=BG
        )
        self.ai_hands_frame.pack()

        self.ai_left_button = tk.Button(
            self.ai_hands_frame,
            text="",
            font=("Times New Roman", 15),
            width=13,
            height=4,
            fg="black",
            bg="white",
            activebackground="white",
            activeforeground="black",
            relief="flat",
            bd=0,
            command=lambda: self.attack_selected_hand(0)
        )
        self.ai_left_button.grid(
            row=0,
            column=0,
            padx=12
        )

        self.ai_right_button = tk.Button(
            self.ai_hands_frame,
            text="",
            font=("Times New Roman", 15),
            width=13,
            height=4,
            fg="black",
            bg="white",
            activebackground="white",
            activeforeground="black",
            relief="flat",
            bd=0,
            command=lambda: self.attack_selected_hand(1)
        )
        self.ai_right_button.grid(
            row=0,
            column=1,
            padx=12
        )

        self.player_label = tk.Label(
            root,
            text="Player",
            font=("Times New Roman", 17, "bold"),
            fg="white",
            bg=BG
        )
        self.player_label.pack(
            pady=(45, 12)
        )

        self.player_hands_frame = tk.Frame(
            root,
            bg=BG
        )
        self.player_hands_frame.pack()

        self.player_left_button = tk.Button(
            self.player_hands_frame,
            text="",
            font=("Times New Roman", 15),
            width=13,
            height=4,
            fg="black",
            bg="white",
            activebackground="white",
            activeforeground="black",
            relief="flat",
            bd=0,
            command=lambda: self.select_player_hand(0)
        )
        self.player_left_button.grid(
            row=0,
            column=0,
            padx=12
        )

        self.player_right_button = tk.Button(
            self.player_hands_frame,
            text="",
            font=("Times New Roman", 15),
            width=13,
            height=4,
            fg="black",
            bg="white",
            activebackground="white",
            activeforeground="black",
            relief="flat",
            bd=0,
            command=lambda: self.select_player_hand(1)
        )
        self.player_right_button.grid(
            row=0,
            column=1,
            padx=12
        )

        self.split_button = tk.Button(
            root,
            text="Split",
            font=("Times New Roman", 13),
            width=16,
            height=2,
            fg="black",
            bg="white",
            activebackground="white",
            activeforeground="black",
            disabledforeground="black",
            relief="flat",
            bd=0,
            command=self.show_split_options
        )
        self.split_button.pack(
            pady=(35, 10)
        )

        self.message_label = tk.Label(
            root,
            text="",
            font=("Times New Roman", 12),
            fg="white",
            bg=BG
        )
        self.message_label.pack()

        self.update_display()

        if self.game.turn == "ai":
            self.root.after(
                700,
                self.ai_turn
            )

    def style_hand_button(self, button, value, selected=False):
        label = "Left" if button in (
            self.ai_left_button,
            self.player_left_button
        ) else "Right"

        if value == 0:
            button.config(
                text=f"{label}\n[out]",
                fg=DEAD_FG,
                bg=DEAD_BG,
                activebackground=DEAD_BG,
                activeforeground=DEAD_FG,
                highlightbackground=DEAD_BORDER,
                highlightthickness=1,
                relief="flat",
                bd=0,
                state="disabled",
                disabledforeground=DEAD_FG
            )
            return

        if selected:
            button.config(
                text=f"{label}\n[{value}]",
                fg=SELECTED_FG,
                bg=SELECTED_BG,
                activebackground=SELECTED_BG,
                activeforeground=SELECTED_FG,
                disabledforeground=SELECTED_FG,
                highlightthickness=0,
                relief="flat",
                bd=0
            )
        else:
            button.config(
                text=f"{label}\n[{value}]",
                fg=LIVE_FG,
                bg=LIVE_BG,
                activebackground=LIVE_BG,
                activeforeground=LIVE_FG,
                disabledforeground=LIVE_FG,
                highlightthickness=0,
                relief="flat",
                bd=0
            )

    def update_display(self):
        selected_left = self.selected_hand == 0
        selected_right = self.selected_hand == 1

        moves_remaining = self.game.max_turns - self.game.turn_count

        self.moves_label.config(
            text=f"Moves remaining: {moves_remaining}"
        )

        self.style_hand_button(
            self.ai_left_button,
            self.game.ai[0]
        )

        self.style_hand_button(
            self.ai_right_button,
            self.game.ai[1]
        )

        self.style_hand_button(
            self.player_left_button,
            self.game.player[0],
            selected=selected_left
        )

        self.style_hand_button(
            self.player_right_button,
            self.game.player[1],
            selected=selected_right
        )

        if self.game.turn == "player":
            self.turn_label.config(
                text="Your turn"
            )

            if self.ai_thinking:
                self.split_button.config(
                    state="disabled"
                )

                self.player_left_button.config(
                    state="disabled"
                )

                self.player_right_button.config(
                    state="disabled"
                )

                self.ai_left_button.config(
                    state="disabled"
                )

                self.ai_right_button.config(
                    state="disabled"
                )

                return

            self.split_button.config(
                state="normal"
            )

            if self.game.player[0] != 0:
                self.player_left_button.config(
                    state="normal"
                )

            if self.game.player[1] != 0:
                self.player_right_button.config(
                    state="normal"
                )

            if self.game.ai[0] != 0:
                self.ai_left_button.config(
                    state="normal"
                )

            if self.game.ai[1] != 0:
                self.ai_right_button.config(
                    state="normal"
                )

            if self.selected_hand is not None:
                self.message_label.config(
                    text="Choose an opponent hand."
                )
            elif self.message_label.cget("text") == "":
                self.message_label.config(
                    text="Select a hand."
                )

        else:
            self.turn_label.config(
                text="AI turn"
            )

            self.split_button.config(
                state="disabled"
            )

            self.player_left_button.config(
                state="disabled"
            )

            self.player_right_button.config(
                state="disabled"
            )

            self.ai_left_button.config(
                state="disabled"
            )

            self.ai_right_button.config(
                state="disabled"
            )

    def select_player_hand(self, hand):
        if self.game.turn != "player":
            return

        if self.ai_thinking:
            return

        if self.game.player[hand] == 0:
            self.message_label.config(
                text="That hand is out."
            )
            return

        if self.selected_hand == hand:
            self.selected_hand = None
            self.update_display()
            return

        self.selected_hand = hand
        self.update_display()

    def attack_selected_hand(self, target):
        if self.selected_hand is None:
            self.message_label.config(
                text="Select one of your hands first."
            )
            return

        if self.game.turn != "player":
            return

        if self.ai_thinking:
            return

        move = None

        for legal_move in self.game.get_legal_moves():
            if (
                legal_move.move_type == "attack"
                and legal_move.source == self.selected_hand
                and legal_move.target == target
            ):
                move = legal_move
                break

        if move is None:
            self.message_label.config(
                text="That move is not available."
            )
            return

        if not self.game.apply_move(move):
            self.message_label.config(
                text="That move is not available."
            )
            return

        self.selected_hand = None

        self.message_label.config(
            text=""
        )

        self.update_display()

        if self.game.get_winner() is not None:
            self.finish_game()
            return

        if self.game.is_draw():
            self.finish_draw()
            return

        self.root.after(
            700,
            self.ai_turn
        )

    def show_split_options(self):
        if self.game.turn != "player":
            return

        if self.ai_thinking:
            return

        window = tk.Toplevel(
            self.root
        )

        window.title("Split")
        window.geometry("340x380")
        window.configure(
            bg=BG
        )
        window.resizable(
            False,
            False
        )

        label = tk.Label(
            window,
            text="Choose your new hands",
            font=("Times New Roman", 16, "bold"),
            fg="white",
            bg=BG
        )
        label.pack(
            pady=22
        )

        moves = self.game.get_legal_moves()

        for move in moves:
            if move.move_type != "split":
                continue

            left, right = move.new_hands

            button = tk.Button(
                window,
                text=f"Left [{left}]   Right [{right}]",
                font=("Times New Roman", 13),
                width=24,
                height=2,
                fg="black",
                bg="white",
                activebackground="white",
                activeforeground="black",
                relief="flat",
                bd=0,
                command=lambda move=move: self.make_split(
                    move,
                    window
                )
            )

            button.pack(
                pady=6
            )

    def make_split(self, move, window):
        if not self.game.apply_move(move):
            self.message_label.config(
                text="That split is not available."
            )
            return

        window.destroy()

        self.selected_hand = None

        self.message_label.config(
            text=""
        )

        self.update_display()

        if self.game.get_winner() is not None:
            self.finish_game()
            return

        if self.game.is_draw():
            self.finish_draw()
            return

        self.root.after(
            700,
            self.ai_turn
        )

    def ai_turn(self):
        if self.game.turn != "ai":
            return

        self.ai_thinking = True

        self.update_display()

        move = self.ai.choose_move(
            self.game
        )

        if move is None:
            self.ai_thinking = False

            self.message_label.config(
                text="No legal moves remain."
            )

            self.update_display()

            return

        if move.move_type == "attack":
            source = move.source
            target = move.target

            source_side = "Left" if source == 0 else "Right"
            target_side = "Left" if target == 0 else "Right"

            if not self.game.apply_move(move):
                self.ai_thinking = False

                self.root.after(
                    100,
                    self.ai_turn
                )

                return

            if self.game.player[target] == 0:
                self.message_label.config(
                    text=f"AI attacked your {target_side} hand with its {source_side} hand. Your {target_side} hand is out."
                )
            else:
                self.message_label.config(
                    text=f"AI attacked your {target_side} hand with its {source_side} hand."
                )

        elif move.move_type == "split":
            left, right = move.new_hands

            if not self.game.apply_move(move):
                self.ai_thinking = False

                self.root.after(
                    100,
                    self.ai_turn
                )

                return

            self.message_label.config(
                text=f"AI split its hands into Left [{left}] and Right [{right}]."
            )

        self.update_display()

        if self.game.get_winner() is not None:
            self.ai_thinking = False
            self.finish_game()
            return

        if self.game.is_draw():
            self.ai_thinking = False
            self.finish_draw()
            return

        self.root.after(
            1200,
            self.enable_player_turn
        )

    def enable_player_turn(self):
        self.ai_thinking = False
        self.update_display()

    def finish_game(self):
        winner = self.game.get_winner()

        if winner == "player":
            self.turn_label.config(
                text="You win!"
            )
        else:
            self.turn_label.config(
                text="AI wins!"
            )

        self.message_label.config(
            text=""
        )

        self.split_button.config(
            state="disabled"
        )

        self.player_left_button.config(
            state="disabled"
        )

        self.player_right_button.config(
            state="disabled"
        )

        self.ai_left_button.config(
            state="disabled"
        )

        self.ai_right_button.config(
            state="disabled"
        )

    def finish_draw(self):
        self.turn_label.config(
            text="Draw!"
        )

        self.message_label.config(
            text="The 100-turn limit was reached."
        )

        self.split_button.config(
            state="disabled"
        )

        self.player_left_button.config(
            state="disabled"
        )

        self.player_right_button.config(
            state="disabled"
        )

        self.ai_left_button.config(
            state="disabled"
        )

        self.ai_right_button.config(
            state="disabled"
        )

    def go_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        build_start_screen(self.root)

    def quit_game(self):
        self.root.destroy()


def show_game_rules(root):
    window = tk.Toplevel(root)
    window.title("Game Rules")
    window.geometry("460x600")
    window.configure(bg=BG)
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="Game Rules",
        font=("Times New Roman", 20, "bold"),
        fg="white",
        bg=BG
    )
    title.pack(
        pady=(26, 16)
    )

    rules = [
        "Each player starts with 1 finger up on each hand.",
        "On your turn, choose one of your hands and tap an opponent's hand.",
        "The opponent's hand gains the number of fingers on your attacking hand.",
        "A hand with 5 or more fingers goes out and becomes 0.",
        "Instead of attacking, you can split your fingers between your two hands.",
        "Splits can be even or uneven, but the total number of fingers must stay the same.",
        "A hand that is out can come back through a split.",
        "You lose when both of your hands are out.",
        "The AI follows the same rules and will tell you what move it makes.",
        "The game must finish within 100 turns, including turns taken by both players. If 100 turns are reached without a winner, the game ends in a draw.",
    ]

    rules_frame = tk.Frame(
        window,
        bg=BG
    )
    rules_frame.pack(
        padx=32,
        pady=5,
        fill="both",
        expand=True
    )

    for i, rule in enumerate(rules, start=1):
        line = tk.Label(
            rules_frame,
            text=f"{i}. {rule}",
            font=("Times New Roman", 13),
            fg="white",
            bg=BG,
            justify="left",
            wraplength=380,
            anchor="w"
        )
        line.pack(
            anchor="w",
            pady=5
        )

    close_button = tk.Button(
        window,
        text="Close",
        font=("Times New Roman", 13),
        width=14,
        height=2,
        fg="black",
        bg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        command=window.destroy
    )
    close_button.pack(
        pady=20
    )

def build_start_screen(root):
    root.title("Sticks")
    root.geometry("500x500")
    root.configure(
        bg=BG
    )
    root.resizable(
        False,
        False
    )

    title_label = tk.Label(
        root,
        text="Sticks",
        font=("Times New Roman", 32, "bold"),
        fg="white",
        bg=BG
    )
    title_label.pack(
        pady=(80, 20)
    )

    difficulty_label = tk.Label(
        root,
        text="Choose difficulty",
        font=("Times New Roman", 15, "bold"),
        fg="white",
        bg=BG
    )
    difficulty_label.pack(
        pady=(0, 30)
    )

    def start_selected_game(difficulty):
        for widget in root.winfo_children():
            widget.destroy()

        SticksGUI(
            root,
            difficulty
        )

    easy_button = tk.Button(
        root,
        text="Easy",
        font=("Times New Roman", 13),
        width=16,
        height=2,
        fg="black",
        bg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        command=lambda: start_selected_game(1)
    )
    easy_button.pack(
        pady=7
    )

    medium_button = tk.Button(
        root,
        text="Medium",
        font=("Times New Roman", 13),
        width=16,
        height=2,
        fg="black",
        bg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        command=lambda: start_selected_game(2)
    )
    medium_button.pack(
        pady=7
    )

    hard_button = tk.Button(
        root,
        text="Hard",
        font=("Times New Roman", 13),
        width=16,
        height=2,
        fg="black",
        bg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        command=lambda: start_selected_game(3)
    )
    hard_button.pack(
        pady=7
    )

    game_rules_button = tk.Button(
        root,
        text="Game Rules",
        font=("Times New Roman", 13),
        width=16,
        height=2,
        fg=NAV_FG,
        bg=NAV_BG,
        activeforeground=NAV_FG,
        activebackground=NAV_BG,
        relief="flat",
        bd=0,
        command=lambda: show_game_rules(root)
    )
    game_rules_button.pack(
        pady=(28, 0)
    )

def start_game():
    root = tk.Tk()
    build_start_screen(root)
    root.mainloop()

if __name__ == "__main__":
    start_game()