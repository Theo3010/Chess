import itertools
from piece import piecesType, piecesColor, piece
import numpy as np



class vaildmoves:
    def __init__(self, game) -> None:
        self.SquaresToEdge = self.Calculate_Squares_To_Edge()
        self.Direction = [8, -8, -1, 1, 7, -7, 9, -9]
        self.game = game

    def Calculate_Squares_To_Edge(self) -> list:
        SquaresToEdge: list[list[int]] = []
        for rank, file in itertools.product(range(8), range(8)):
            North = 7 - rank
            south = rank
            west = file
            east = 7 - file

            SquaresToEdge.append(
                [
                    North,
                    south,
                    west,
                    east,
                    min(North, west),
                    min(south, east),
                    min(North, east),
                    min(south, west),
                ]
            )
        return SquaresToEdge

    def calc_moves(self, Piece, pieces: list, king: bool = True, check: bool = True) -> list:
        if Piece.type == piecesType.PAWN:
            moves = self.pawnmoves(Piece, pieces)
        elif Piece.type == piecesType.KNIGHT:
            moves = self.knightmoves(Piece, pieces)
        elif Piece.type == piecesType.KING and king:
            moves = self.kingmoves(Piece, pieces)
        else:
            moves = self.slidingmoves(Piece, pieces)
        
        if check and moves:
            return self.check_for_check(moves, Piece, pieces)
        
        return moves

    
    def check_for_check(self, moves: list, Piece, pieces: list):

        opponentColor = (
            piecesColor.BLACK if self.game.IsWhiteTurn else piecesColor.WHITE
        )

        for move in moves:
            piecescopy = pieces.copy()
            piecescopy[move] = Piece

            EnemyMoves = self.findAllMoves(opponentColor, piecescopy, check = False)[1]
            # print(move, "\n", list(move in EnemyMove for EnemyMove in EnemyMoves))

            if any(move in EnemyMove for EnemyMove in EnemyMoves):
                moves.remove(move)

        return moves

    def slidingmoves(self, Piece, pieces: list):
        startdirection = 4 if Piece.type == piecesType.BISHOP else 0
        enddirection = 4 if Piece.type == piecesType.ROOK else 8

        moves = []
        for direction in range(startdirection, enddirection):
            for i in range(self.SquaresToEdge[Piece.pos][direction]):

                targetsquare = Piece.pos + self.Direction[direction] * (i + 1)

                PieceOnSquare = pieces[targetsquare]

                if PieceOnSquare.color == Piece.color:
                    break

                moves.append(targetsquare)

                if PieceOnSquare.color != piecesColor.NONE:
                    break
        return moves

    def pawnmoves(self, Piece, pieces: list) -> list:
        pawnmovesUP = [-9, -7, -8, -16]
        pawnmovesDOWN = [9, 7, 8, 16]

        moveColor = piecesColor.WHITE if self.game.IsWhiteTurn else piecesColor.BLACK
        opponentColor = (
            piecesColor.BLACK if self.game.IsWhiteTurn else piecesColor.WHITE
        )

        pawnmoves = pawnmovesUP if moveColor == piecesColor.WHITE else pawnmovesDOWN

        moves = []
        for move in pawnmoves:
            targetsquare = Piece.pos + move

            # Check for out of bonce for rows
            if targetsquare >= len(pieces) or targetsquare < 0:
                continue

            PieceOnSquare = pieces[targetsquare]

            # Check for out of bonce colums
            if not self.check_for_colums(1, targetsquare, Piece.pos):
                continue

            if move in [9, 7, -9, -7]:
                if PieceOnSquare.color == opponentColor:
                    moves.append(targetsquare)
                continue

            if PieceOnSquare.color == piecesColor.NONE:
                if Piece.has_moved and move in [16, -16]:
                    continue

                moves.append(targetsquare)
                continue

            break

        return moves

    def kingmoves(self, Piece, pieces: list) -> list:
        kingmoves = [1, 7, 8, 9, -1, -7, -8, -9]

        opponentColor = (
            piecesColor.BLACK if self.game.IsWhiteTurn else piecesColor.WHITE
        )

        # EnemyMoves = self.findAllMoves(opponentColor, pieces)[1]

        moves = []
        for move in kingmoves:
            targetsquare = Piece.pos + move

            if targetsquare > len(pieces) or targetsquare < 0:
                continue

            # if any(targetsquare in EnemyMove for EnemyMove in EnemyMoves):
            #     continue

            PieceOnSquare = pieces[targetsquare]

            if PieceOnSquare.color == Piece.color:
                continue

            if not self.check_for_colums(1, targetsquare, Piece.pos):
                continue

            moves.append(targetsquare)

    def knightmoves(self, Piece, pieces: list) -> list:
        knightmoves = [-10, -6, -17, -15, 10, 6, 17, 15]

        moves = []
        for move in knightmoves:
            targetsquare = Piece.pos + move

            if targetsquare >= len(pieces) or targetsquare < 0:
                continue

            PieceOnSquare = pieces[targetsquare]

            if not self.check_for_colums(2, targetsquare, Piece.pos):
                continue

            if PieceOnSquare.color == Piece.color:
                continue

            moves.append(targetsquare)
        return moves

    def check_for_colums(self, numOfColums: int, targetsquare: int, PiecePos: int):
        possiblePosition = targetsquare % 8 + 1
        currentPostion = PiecePos % 8 + 1

        if (np.abs(possiblePosition - currentPostion) > numOfColums):
            return False
        return True
    
    def findAllMoves(self, color, pieces, check: bool = True):
        AlivePieces = []
        possibleMoves = []
        selectedPieces = []

        for piece in pieces:
            if piece.color == color:
                AlivePieces.append(piece)

        for selectedPiece in AlivePieces:
            moves = vaildmoves(self.game).calc_moves(
                selectedPiece, pieces, False, check)
           
            if not moves:
                continue
            
            possibleMoves.append(moves)
            selectedPieces.append(selectedPiece)

        return selectedPieces, possibleMoves

if __name__ == "__main__":
    v = vaildmoves.pawnmoves()
    print(v)
