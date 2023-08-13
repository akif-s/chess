import pygame
from sound import Sound


class Piece:
    def __init__(self, type, color, file, rank, scale_factor, board) -> None:
        self.type = type  # the type of the piece.
        self.color = color  # the color of the piece
        self.file = file  # the file which the piece is over
        self.rank = rank  # the rank which the piece is over
        self.scale_factor = scale_factor
        self.board = board

        self.lastMoved = -1 
        self.isEnPassant = False

        self.square_index = (self.rank - 1) * 8 + (self.file - 1)

        self.name = {"p": "pawn", "k": "king", "b": "bishop", "n": "knight",
                     "q": "queen", "r": "rook"}[self.type.lower()]  # full name of the piece

        self.pfile = file
        self.prank = rank

        self.coordinate = [0, 0]

        self.is_grabbed = False
        self.is_moved = False

        # loads the image and scales by given factor.
        self.img = pygame.transform.scale_by(pygame.image.load(
            f"pieces/{self.color}-{self.type}.png"), self.scale_factor)

        self.valid_moves = []

    # returns the general info about the piece object.

    def __str__(self) -> str:
        return f"type: {self.name}\ncolor: {self.color}\nfile: {self.file}\nrank: {self.rank}\nsquare index: {self.square_index}\nis grabbed:{self.is_grabbed}\nis en passant: {self.isEnPassant}\n---------"

    def draw(self, board, pointer):
        tile_size = board.surface.get_width() / 8

        # x-coordinate of the piece calculated from the file of the piece
        self.coordinate[0] = (
            (8 - self.file) * tile_size
            if board.rotation == 1
            else (self.file - 1) * tile_size
        )

        # y-coordinate of the piece calculated from the rank of the piece
        self.coordinate[1] = (
            (8 - self.rank) * tile_size
            if board.rotation == 0
            else (self.rank - 1) * tile_size
        )

        if self.is_grabbed:
            self.file = pointer.file
            self.rank = pointer.rank
            self.coordinate[0] = pointer.x - self.img.get_size()[0]/2
            self.coordinate[1] = pointer.y - self.img.get_size()[1]/2

        board.surface.blit(
            self.img,
            pygame.Rect(
                self.coordinate[0],
                self.coordinate[1],
                tile_size,
                tile_size,
            ),
        )

    def Move(self, targetSquare, moveCount, isMoved=True):
        Sound.PlayMove()
        self.lastMoved = moveCount
        
        file, rank = Piece.SquareIndexToFileAndRank(targetSquare)

        self.file = file
        self.rank = rank

        self.square_index = targetSquare

        self.is_grabbed = False
        self.is_moved = isMoved

    def Eat(self, targetPiece):
        Sound.PlayCapture()
        targetPiece.Destroy()

    def Destroy(self):
        self.board.destroyPiece(self)

    def reset(self):
        self.rank = self.prank
        self.file = self.pfile

    def is_sliding(piece):
        if piece.type in ["q", "r", "b"]:
            return True
        return False

    def IsColour(piece, color):
        if piece.color == color:
            return True
        return False

    def IsType(piece, type):
        if piece.type == type:
            return True
        return False
    
    def SquareIndexToFileAndRank(n) -> int:
        file = (n%8) + 1
        rank = (n - file + 1)//8 + 1
        return file, rank

    def ToSquareIndex(file, rank) -> int:
        return (rank-1)*8 + file - 1

    # Need to check BEFORE the move has been made.
    def IsEnPassant(piece, moveCount):
        if piece.type != "p":
            return False

        # If the pawn moved double
        if abs(piece.prank - piece.rank) == 2 and moveCount - piece.lastMoved == 0:
            piece.isEnPassant = True
            return True

        piece.isEnPassant = False
        return False

