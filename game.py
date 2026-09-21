import copy
import random

from move import Move

class GameState:

    def __init__(self):
        self.player = [1, 1]
        self.ai = [1, 1]

        if random.randint(0, 1) == 0:
            self.turn = "player"
        else:
            self.turn = "ai"

        self.turn_count = 0
        self.max_turns = 100

    def copy(self):
        return copy.deepcopy(self)

    def get_resulting_state(self, move):
        if move.move_type == "attack":
            if move.source not in (0, 1):
                return None

            if move.target not in (0, 1):
                return None

            if self.turn == "player":
                attacker = self.player
                target = self.ai
            else:
                attacker = self.ai
                target = self.player

            if attacker[move.source] == 0:
                return None

            if target[move.target] == 0:
                return None

            new_value = target[move.target] + attacker[move.source]

            if new_value >= 5:
                new_value = 0

            if self.turn == "player":
                new_player = list(self.player)
                new_ai = list(self.ai)
                new_ai[move.target] = new_value
            else:
                new_player = list(self.player)
                new_ai = list(self.ai)
                new_player[move.target] = new_value

            return (
                tuple(new_player),
                tuple(new_ai)
            )

        if move.move_type == "split":
            if move.new_hands is None:
                return None

            left_num, right_num = move.new_hands

            if left_num < 0 or left_num > 4:
                return None

            if right_num < 0 or right_num > 4:
                return None

            if self.turn == "player":
                hands = self.player
            else:
                hands = self.ai

            if hands[0] + hands[1] != left_num + right_num:
                return None

            if hands == [left_num, right_num]:
                return None

            if self.turn == "player":
                new_player = [left_num, right_num]
                new_ai = list(self.ai)
            else:
                new_player = list(self.player)
                new_ai = [left_num, right_num]

            return (
                tuple(new_player),
                tuple(new_ai)
            )

        return None

    def get_legal_moves(self):
        moves = []

        if self.turn == "player":
            attacker = self.player
            target = self.ai
        else:
            attacker = self.ai
            target = self.player

        for attack_hand in range(2):
            for target_hand in range(2):
                if attacker[attack_hand] == 0:
                    continue

                if target[target_hand] == 0:
                    continue

                moves.append(
                    Move(
                        "attack",
                        source=attack_hand,
                        target=target_hand
                    )
                )

        total = attacker[0] + attacker[1]

        for left in range(5):
            right = total - left

            if right < 0 or right > 4:
                continue

            if [left, right] == attacker:
                continue

            moves.append(
                Move(
                    "split",
                    new_hands=(left, right)
                )
            )

        return moves

    def get_winner(self):
        if self.player == [0, 0]:
            return "ai"

        if self.ai == [0, 0]:
            return "player"

        return None

    def is_draw(self):
        return self.turn_count >= self.max_turns and self.get_winner() is None

    def switch_turns(self):
        if self.turn == "player":
            self.turn = "ai"
        else:
            self.turn = "player"

    def attack_on_turn(self, attack_hand, target_hand):
        move = Move(
            "attack",
            source=attack_hand,
            target=target_hand
        )

        state = self.get_resulting_state(move)

        if state is None:
            return False

        if self.turn == "player":
            self.ai[target_hand] = state[1][target_hand]
        else:
            self.player[target_hand] = state[0][target_hand]

        self.turn_count += 1
        self.switch_turns()

        return True

    def split(self, left_num, right_num):
        move = Move(
            "split",
            new_hands=(left_num, right_num)
        )

        state = self.get_resulting_state(move)

        if state is None:
            return False

        if self.turn == "player":
            self.player = [left_num, right_num]
        else:
            self.ai = [left_num, right_num]

        self.turn_count += 1
        self.switch_turns()

        return True

    def apply_move(self, move):
        if move.move_type == "attack":
            return self.attack_on_turn(
                move.source,
                move.target
            )

        if move.move_type == "split":
            return self.split(
                move.new_hands[0],
                move.new_hands[1]
            )

        return False