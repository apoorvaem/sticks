from dataclasses import dataclass

@dataclass(frozen=True)
class Move:
    move_type: str
    source: int | None = None
    target: int | None = None
    new_hands: tuple[int, int] | None = None

    def __repr__(self):
        return (
            f"Move(move_type = '{self.move_type}', "
            f"source = {self.source}, "
            f"target = {self.target}, "
            f"new_hands = {self.new_hands})"
        )