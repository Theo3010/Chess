from dataclasses import dataclass
from enum import Enum
import pygame as pg
from typing_extensions import Self


class piecesColor(Enum):
    WHITE = "White"
    BLACK = "Black"
    NONE = "None"


class piecesType(Enum):
    KING = "King"
    QUEEN = "Queen"
    ROOK = "Rook"
    KNIGHT = "Knight"
    BISHOP = "Bishop"
    PAWN = "pawn"
    NONE = "None"


@dataclass(unsafe_hash=True)
class piece:
    pos: int = None
    type: piecesType = piecesType.NONE
    color: piecesColor = piecesColor.NONE
    has_moved: bool = False
    rect: pg.Rect = None

    def promote(self, newPicesType: piecesType) -> None:
        self.type = newPicesType

    def move(self, move: int, pieces: list) -> Self:
        pieces[self.pos] = piece(self.pos)
        pieces[move] = self

        self.pos = move
        self.has_moved = True

    def image(self) -> str:
        return f"ChessPieces/{self.color.value}{self.type.value}.png"

    def set_rect(self, rect: pg.Rect) -> None:
        self.rect = rect


FENTOTYPE: dict = {
    "p": piecesType.PAWN,
    "b": piecesType.BISHOP,
    "n": piecesType.KNIGHT,
    "r": piecesType.ROOK,
    "q": piecesType.QUEEN,
    "k": piecesType.KING,
}
