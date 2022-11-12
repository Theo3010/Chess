import sys
from tabnanny import check
import pygame as pg
from settings import *
from board import *
from pieces import Pieces
from ChessEngine import ChessEngine


class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.IsWhiteTurn: bool = True
        self.game_over: bool = False
        self.new_game()

    def new_game(self):
        self.board = Board(self)
        self.pieces = Pieces(self)
        self.ChessEnigne = ChessEngine(self, self.pieces)

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps():.1f}")

        self.pieces.update()
        # self.ChessEnigne.update()

    def draw(self):
        # self.screen.fill("black")
        self.board.draw()
        self.pieces.draw()

    def check_events(self):
        for events in pg.event.get():
            if events.type == pg.QUIT or events.type == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

    def run(self):
        while not self.game_over:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
