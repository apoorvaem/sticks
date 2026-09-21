from game import GameState


game = GameState()

game.player = [1, 1]
game.ai = [1, 1]
game.turn = "player"

# Pretend this state has already happened
game.history.add(
    ((0, 2), (1, 1), "ai")
)

print("HISTORY BEFORE SPLIT:")
print(game.history)

print()
print("BEFORE")
print("Player:", game.player)
print("AI:", game.ai)
print("Turn:", game.turn)

result = game.split(0, 2)

print()
print("AFTER")
print("Move accepted:", result)
print("Player:", game.player)
print("AI:", game.ai)
print("Turn:", game.turn)