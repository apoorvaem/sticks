import random

class GameState:

    def __init__(self):
        self.player = [1,1]
        self.ai = [1,1]

        if random.randint(0,1) == 0:
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

    def get_winner(self):
        if self.player == [0,0]:
            return "ai"
        
        if self.ai == [0,0]:
            return "player"
        
        return None
    
    def switch_turns(self):
        if self.turn == "player":
            self.turn = "ai"
        else:
            self.turn = "player"

        self.save_state()

    def attack_on_turn(self, attack_hand, target_hand):
        if self.turn == "player":
            attacker = self.player
            target = self.ai
        else:
            attacker = self.ai
            target = self.player

        if attacker[attack_hand] == 0:
            return False
        
        if target[target_hand] == 0:
            return False
        
        target[target_hand] = target[target_hand] + attacker[attack_hand]

        if target[target_hand] >= 5:
            target[target_hand] = 0

        self.switch_turns()

        return True
    
    def split(self, left_num, right_num):
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
        
        self_hands = [left_num, right_num]

        hands[0] = self_hands[0]
        hands[1] = self_hands[1]

        self.switch_turns()

        return True