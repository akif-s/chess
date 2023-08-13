from board import Move

""" if self.move.isRook:
        self.piece.square_index = self.move.targetSquare
        self.move.targetRook.square_index = self.move.rookTargetSquare

        self.piece.is_moved = True
        self.move.targetRook.is_moved = True

        self.piece.is_grabbed = False
        self.piece = None

    if self.piece.is_grabbed:

        targetPiece = board.square[self.move.targetSquare] if self.move.targetSquare in board.square.keys(
        ) else None

        if targetPiece != None:
            self.piece.Eat(targetPiece)

        self.piece.square_index = self.move.targetSquare
        self.piece.is_moved = True
        self.piece.is_grabbed = False
        self.piece = None """


class Pointer:
    def __init__(self, rotation, surface) -> None:
        self.rotation = rotation
        self.surface = surface
        self.pos = (0, 0)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.file = 0
        self.str_file = ""
        self.rank = 0

        self.press = False
        self.toggle = False
        self.drag = False

        self.piece = None

        self.move = Move(0, 0)

    def __str__(self) -> str:
        return f"[{self.file},{self.rank}] {self.str_file}{self.rank}"

    def update_pos(self, pos):
        self.pos = pos  # pos is a tuple or list
        self.x = pos[0]
        self.y = pos[1]

        self.update_tile()

    # Update the tile numbers which cursor is currently over.
    # TO BE CHANGED
    def update_tile(self):
        tile_size = self.surface.get_width() / 8

        self.file = int(
            (self.x + (tile_size - self.x % tile_size)) / tile_size)
        self.file = (9 - self.file) if self.rotation == 1 else self.file

        self.rank = int(
            (self.y + (tile_size - self.y % tile_size)) / tile_size)
        self.rank = (9 - self.rank) if self.rotation == 0 else self.rank

        self.str_file = "abcdefgh"[self.file - 1]

    def get_pos(self):
        return self.pos

    def get_tile(self):
        return [self.file, self.rank]

    # TO BE CHANGED. make the piece finding from board.square
    def grab_piece(self, pieces, board):
        board.generate_moves()
        for piece in pieces:
            if (piece.file == self.file and piece.rank == self.rank and piece.color == board.color_to_move):

                self.move.startSquare = piece.square_index

                # Paint the grabbed square to indicate.
                board.paint_square(piece.square_index, (240, 235, 96))

                # Grabbed location of the file
                piece.pfile = piece.file
                piece.prank = piece.rank

                self.piece = piece
                piece.is_grabbed = True

                board.change_color()

    def release_piece(self, board):
        if self.piece != None:
            self.move.targetSquare = (self.rank - 1)*8 + (self.file - 1)

            if self.move in board.moves:
                board.MakeMove(self.move)
                self.piece = None

            else:
                board.change_color()
                self.piece.reset()
                self.piece.is_grabbed = False
                self.piece = None
