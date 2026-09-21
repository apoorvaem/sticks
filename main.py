from game import GameState

game = GameState()

print("Player:", game.player)
print("AI:", game.ai)
print("Turn:", game.turn)
print("Legal moves:", game.get_legal_moves())