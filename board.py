from __future__ import annotations
import itertools
import pygame as pg
from settings import *


class Game:
    def __init__(self) -> None:
        self.screen = pg.display


class Board:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.board = [0] * 64
        self.GREEN = (118, 150, 86)
        self.WHITE = (238, 238, 210)

    def draw(self):
        letters: list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for x, y in itertools.product(range(8), range(8)):
            if (x + y) % 2 == 0:
                pg.draw.rect(
                    self.game.screen,
                    self.WHITE,
                    (
                        0 + SQUAREWIDTH * x,
                        0 + SQUAREHEIGHT * y,
                        SQUAREWIDTH,
                        SQUAREHEIGHT,
                    ),
                )  # WHITE
            else:
                pg.draw.rect(
                    self.game.screen,
                    self.GREEN,
                    (
                        0 + SQUAREWIDTH * x,
                        0 + SQUAREHEIGHT * y,
                        SQUAREWIDTH,
                        SQUAREHEIGHT,
                    ),
                )  # GREEN
            if y % 2 == 0:
                self.draw_text(
                    self.game,
                    str(8 - y),
                    self.GREEN,
                    self.WHITE,
                    8,
                    15 + SQUAREHEIGHT * y,
                )  # draw numbers 8,6,4,2 | GREEN
            else:
                self.draw_text(
                    self.game,
                    str(8 - y),
                    self.WHITE,
                    self.GREEN,
                    8,
                    15 + SQUAREHEIGHT * y,
                )  # draw numbers 7,5,3,1 | WHITE

            if x % 2 == 0:
                self.draw_text(
                    self.game,
                    letters[x],
                    self.WHITE,
                    self.GREEN,
                    SQUAREWIDTH * 0.90 + SQUAREWIDTH * x,
                    HEIGHT * 0.98,
                )
            else:
                self.draw_text(
                    self.game,
                    letters[x],
                    self.GREEN,
                    self.WHITE,
                    SQUAREWIDTH * 0.90 + SQUAREWIDTH * x,
                    HEIGHT * 0.98,
                )

    @staticmethod
    def draw_text(
        game: Game,
        msg: str,
        color: tuple[int, int, int],
        backgrund_color: tuple[int, int, int],
        x: int,
        y: int,
    ) -> None:
        """
        Draw text to the screen
        """
        font = pg.font.Font("freesansbold.ttf", TEXTSSIZE)
        text = font.render(msg, True, color, backgrund_color)

        textRect = text.get_rect()
        textRect.center = (x, y)

        game.screen.blit(text, textRect)


if __name__ == "__main__":
    board = Board("a")
    print((board.board))
