class AI:

    def __init__(self, side="ai", depth=1):
        if side not in ("player", "ai"):
            raise ValueError("side must be 'player' or 'ai'")

        self.side = side
        self.depth = depth
        self.nodes_searched = 0

    def choose_move(self, game):
        self.nodes_searched = 0

        moves = game.get_legal_moves()

        if not moves:
            return None

        best_move = None
        best_score = float("-inf")

        alpha = float("-inf")
        beta = float("inf")

        for move in moves:
            new_game = game.copy()

            if not new_game.apply_move(move):
                continue

            score = self.alpha_beta(
                new_game,
                self.depth,
                alpha,
                beta
            )

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        return best_move

    def minimax(self, game, depth):
        self.nodes_searched += 1

        winner = game.get_winner()

        if winner is not None or depth == 0:
            return self.evaluate_state(game)

        moves = game.get_legal_moves()

        if not moves:
            return self.evaluate_state(game)

        if game.turn == self.side:
            best_score = float("-inf")

            for move in moves:
                new_game = game.copy()

                if not new_game.apply_move(move):
                    continue

                score = self.minimax(new_game, depth - 1)
                best_score = max(best_score, score)

            return best_score

        best_score = float("inf")

        for move in moves:
            new_game = game.copy()

            if not new_game.apply_move(move):
                continue

            score = self.minimax(new_game, depth - 1)
            best_score = min(best_score, score)

        return best_score

    def alpha_beta(self, game, depth, alpha, beta):
        self.nodes_searched += 1

        winner = game.get_winner()

        if winner is not None or depth == 0:
            return self.evaluate_state(game)

        moves = game.get_legal_moves()

        if not moves:
            return self.evaluate_state(game)

        if game.turn == self.side:
            best_score = float("-inf")

            for move in moves:
                new_game = game.copy()

                if not new_game.apply_move(move):
                    continue

                score = self.alpha_beta(
                    new_game,
                    depth - 1,
                    alpha,
                    beta
                )

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            return best_score

        best_score = float("inf")

        for move in moves:
            new_game = game.copy()

            if not new_game.apply_move(move):
                continue

            score = self.alpha_beta(
                new_game,
                depth - 1,
                alpha,
                beta
            )

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                break

        return best_score

    def evaluate_state(self, game):
        winner = game.get_winner()

        if winner == self.side:
            return 1000

        opponent = "player" if self.side == "ai" else "ai"

        if winner == opponent:
            return -1000

        if self.side == "ai":
            ai_hands = game.ai
            player_hands = game.player
        else:
            ai_hands = game.ai
            player_hands = game.player

        if self.side == "ai":
            my_hands = ai_hands
            other_hands = player_hands
        else:
            my_hands = player_hands
            other_hands = ai_hands

        my_total = my_hands[0] + my_hands[1]
        other_total = other_hands[0] + other_hands[1]

        my_alive = sum(1 for hand in my_hands if hand > 0)
        other_alive = sum(1 for hand in other_hands if hand > 0)

        my_kills = self.count_kill_opportunities(
            my_hands,
            other_hands
        )

        other_kills = self.count_kill_opportunities(
            other_hands,
            my_hands
        )

        my_threats = self.count_threatened_hands(
            other_hands,
            my_hands
        )

        other_threats = self.count_threatened_hands(
            my_hands,
            other_hands
        )

        finger_score = my_total - other_total

        living_hand_score = my_alive - other_alive

        tactical_score = (
            my_kills - other_kills
        ) * 3

        defensive_score = (
            other_threats - my_threats
        ) * 4

        return (
            finger_score
            + living_hand_score
            + tactical_score
            + defensive_score
        )

    def count_kill_opportunities(self, attacker, target):
        count = 0

        for attack_hand in attacker:
            if attack_hand == 0:
                continue

            for target_hand in target:
                if target_hand == 0:
                    continue

                if attack_hand + target_hand >= 5:
                    count += 1

        return count

    def count_threatened_hands(self, attacker, target):
        count = 0

        for target_hand in target:
            if target_hand == 0:
                continue

            for attack_hand in attacker:
                if attack_hand == 0:
                    continue

                if attack_hand + target_hand >= 5:
                    count += 1
                    break

        return count