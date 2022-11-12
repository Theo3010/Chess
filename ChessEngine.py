import random
from piece import piecesColor
from vaildmoves import vaildmoves


class ChessEngine:
    def __init__(self, game, pieces) -> None:
        self.game = game
        self.pieces = pieces.pieces

    def update(self):
        if not self.game.IsWhiteTurn:
            PiecesAndMoves = list(zip(vaildmoves(self.game).findAllMoves(piecesColor.BLACK, self.pieces)))

            if len(PiecesAndMoves) <= 0:
                self.game_over = True
                print("Black has no moves. White wins")

            selectedPieceAndMove = random.choice(PiecesAndMoves)

            selectedPieceAndMove[0].move(
                random.choice(selectedPieceAndMove[1]), self.pieces)
            self.game.IsWhiteTurn = True
