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

        self.history = set()
        self.save_state()

    def save_state(self):
        state = (
            tuple(self.player),
            tuple(self.ai),
            self.turn
        )

        self.history.add(state)

    def state_exists(self, player, ai, turn):
        state = (
            tuple(player),
            tuple(ai),
            turn
        )

        return state in self.history

    def get_state(self):
        return (
            tuple(self.player),
            tuple(self.ai),
            self.turn
        )

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

                new_target_value = (
                    target[target_hand] + attacker[attack_hand]
                )

                if new_target_value >= 5:
                    new_target_value = 0

                if self.turn == "player":
                    new_player = list(self.player)
                    new_ai = list(self.ai)

                    new_ai[target_hand] = new_target_value
                    new_turn = "ai"

                else:
                    new_player = list(self.player)
                    new_ai = list(self.ai)

                    new_player[target_hand] = new_target_value
                    new_turn = "player"

                if self.state_exists(new_player, new_ai, new_turn):
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

            if self.turn == "player":
                new_player = [left, right]
                new_ai = list(self.ai)
                new_turn = "ai"

            else:
                new_player = list(self.player)
                new_ai = [left, right]
                new_turn = "player"

            if self.state_exists(new_player, new_ai, new_turn):
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

    def switch_turns(self):
        if self.turn == "player":
            self.turn = "ai"
        else:
            self.turn = "player"

    def attack_on_turn(self, attack_hand, target_hand):

        if self.turn == "player":
            attacker = self.player
            target = self.ai
        else:
            attacker = self.ai
            target = self.player

        if attack_hand not in (0, 1):
            return False

        if target_hand not in (0, 1):
            return False

        if attacker[attack_hand] == 0:
            return False

        if target[target_hand] == 0:
            return False

        new_target_value = target[target_hand] + attacker[attack_hand]

        if new_target_value >= 5:
            new_target_value = 0

        if self.turn == "player":
            new_player = list(self.player)
            new_ai = list(self.ai)

            new_ai[target_hand] = new_target_value
            new_turn = "ai"

        else:
            new_player = list(self.player)
            new_ai = list(self.ai)

            new_player[target_hand] = new_target_value
            new_turn = "player"

        if self.state_exists(new_player, new_ai, new_turn):
            return False

        if self.turn == "player":
            self.ai[target_hand] = new_target_value
        else:
            self.player[target_hand] = new_target_value

        self.switch_turns()
        self.save_state()

        return True

    def split(self, left_num, right_num):

        if left_num < 0 or left_num > 4:
            return False

        if right_num < 0 or right_num > 4:
            return False

        if self.turn == "player":
            hands = self.player
        else:
            hands = self.ai

        total_before = hands[0] + hands[1]
        total_after = left_num + right_num

        if total_before != total_after:
            return False

        if hands == [left_num, right_num]:
            return False

        if self.turn == "player":
            new_player = [left_num, right_num]
            new_ai = list(self.ai)
            new_turn = "ai"

        else:
            new_player = list(self.player)
            new_ai = [left_num, right_num]
            new_turn = "player"

        if self.state_exists(new_player, new_ai, new_turn):
            return False

        if self.turn == "player":
            self.player = new_player
        else:
            self.ai = new_ai

        self.switch_turns()
        self.save_state()

        return True