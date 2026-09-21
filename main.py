import os

from game import GameState
from ai import AI

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def hand_name(hand):
    return "Left" if hand == 0 else "Right"

def display_game(game):
    clear_screen()

    print("STICKS")
    print()
    print(f"AI:     Left [{game.ai[0]}]   Right [{game.ai[1]}]")
    print(f"Player: Left [{game.player[0]}]   Right [{game.player[1]}]")
    print()
    print(f"TURN: {game.turn.upper()}")
    print()

def describe_move(move):
    if move.move_type == "attack":
        source = hand_name(move.source)
        target = hand_name(move.target)

        return f"Attack {target} hand with {source} hand"

    left, right = move.new_hands

    return f"Split into Left [{left}], Right [{right}]"

def choose_difficulty():
    print("STICKS")
    print()
    print("Choose difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print()

    while True:
        choice = input("Choice: ").strip()

        if choice == "1":
            return 1

        if choice == "2":
            return 2

        if choice == "3":
            return 3

        print("Please enter 1, 2, or 3.")

def choose_player_move(game):
    moves = game.get_legal_moves()

    print("Your legal moves:")
    print()

    for index, move in enumerate(moves, start=1):
        print(f"{index}. {describe_move(move)}")

    print()

    while True:
        choice = input("Choose a move: ").strip()

        if not choice.isdigit():
            print("Please enter a move number.")
            continue

        move_index = int(choice) - 1

        if 0 <= move_index < len(moves):
            return moves[move_index]

        print("Please choose one of the listed moves.")

def play_game(difficulty):
    game = GameState()
    ai = AI(side="ai", depth=difficulty)

    while game.get_winner() is None:
        display_game(game)

        if game.turn == "player":
            move = choose_player_move(game)

            if game.apply_move(move):
                print()
                print(f"You: {describe_move(move)}")
                input("Press Enter to continue...")
            else:
                print("That move could not be applied.")
                input("Press Enter to try again.")

        else:
            print("AI is thinking...")
            print()

            move = ai.choose_move(game)

            if move is None:
                print("AI could not make a move.")
                break

            if game.apply_move(move):
                print(f"AI: {describe_move(move)}")
                input("Press Enter to continue...")
            else:
                print("AI could not make a move.")
                break

    display_game(game)

    if game.get_winner() == "player":
        print("YOU WIN!")
    elif game.get_winner() == "ai":
        print("AI WINS!")

    print()
    input("Press Enter to exit...")

def main():
    difficulty = choose_difficulty()
    play_game(difficulty)


if __name__ == "__main__":
    main()