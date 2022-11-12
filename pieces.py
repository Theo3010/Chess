from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import itertools
from typing_extensions import Self
import pygame as pg
from settings import *
from vaildmoves import *
from piece import *


class Board:
    pass


class Game:
    pass


class Pieces:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.pieces: list[piece] = self.create_pieces()
        self.FEN_Array(FEN)
        self.selectedPieces: piece = None
        self.moveToSquares = {}

    @staticmethod
    def create_pieces() -> list:
        pieces = []
        for index in range(64):
            pieces.append(piece(index))
        return pieces

    def FEN_Array(self, FEN: str) -> list:
        index: int = 0

        for symbol in FEN:
            if symbol == "/":
                continue
            if symbol.isdigit():
                index += int(symbol)
            else:
                self.pieces[index] = piece(
                    index,
                    FENTOTYPE[symbol.lower()],
                    piecesColor.WHITE if symbol.isupper() else piecesColor.BLACK,
                )
                index += 1

    def draw(self):
        self.moveToSquares = {}
        # key = pg.key.get_pressed()
        # if self.selectedPieces and key[pg.K_d]:
        if self.selectedPieces:
            for index in vaildmoves(self.game).calc_moves(
                self.selectedPieces, self.pieces
            ):
                x, y = index % 8, index // 8
                self.moveToSquares[y * 8 + x] = pg.draw.rect(
                    self.game.screen,
                    (255, 0, 0, 0.5),
                    pg.Rect(
                        (WIDTH // 8 * x) + 5,
                        (HEIGHT // 8 * y) + 5,
                        (HEIGHT // 8) - 10,
                        (WIDTH // 8) - 10,
                    ),
                )

        for y, x in itertools.product(range(8), range(8)):
            if self.pieces[y * 8 + x].type != piecesType.NONE:
                self.pieces[y * 8 + x].set_rect(
                    self.game.screen.blit(
                        self.loadpieces(self.pieces[y * 8 + x]),
                        (SQUAREWIDTH * x + OFFSET_X, SQUAREHEIGHT * y + OFFSET_Y),
                    )
                )

    def loadpieces(self, pieces) -> pg.image:
        return pg.transform.scale(
            pg.image.load(pieces.image()),
            (
                int(WIDTH // 8 * SCALE_X),
                int(HEIGHT // 8 * SCALE_Y),
            ),
        )

    def Check_for_selectedPiece(self):
        colorsTurn = piecesColor.WHITE if self.game.IsWhiteTurn else piecesColor.BLACK

        for piece in self.pieces:
            if piece.rect is None:
                continue

            if (
                piece.rect.collidepoint(pg.mouse.get_pos())
                and pg.mouse.get_pressed()[0] == 1
                and piece.color == colorsTurn
            ):

                self.selectedPieces = piece

    def check_for_moveToSquare(self):
        for index in self.moveToSquares:
            if self.moveToSquares[index]:
                if (
                    self.moveToSquares[index].collidepoint(pg.mouse.get_pos())
                    and pg.mouse.get_pressed()[0] == 1
                    and self.selectedPieces is not None
                ):
                    self.selectedPieces.move(index, self.pieces)
                    self.selectedPieces = None
                    self.game.IsWhiteTurn = not self.game.IsWhiteTurn

    def promote_pawn(self):
        PromoteSquare = list(range(0, 8)) + list(range(64 - 8, 64))
        promoteType = None

        key = pg.key.get_pressed()
        if key[pg.K_q]:
            promoteType = piecesType.QUEEN

        if key[pg.K_n]:
            promoteType = piecesType.KNIGHT

        if key[pg.K_b]:
            promoteType = piecesType.BISHOP

        for piece in self.pieces:
            if piece.type != piecesType.PAWN:
                continue

            if piece.pos in PromoteSquare:
                if promoteType:
                    piece.promote(promoteType)

    def update(self):
        self.Check_for_selectedPiece()
        self.check_for_moveToSquare()
        self.promote_pawn()
