import pygame
from pygame.locals import *
from piece import Piece
from move import Move


class Board:
    def __init__(self, color1, color2, altColor1, altColor2, surface, rotation=0):
        self.color1 = color1
        self.color2 = color2
        self.altColor1 = altColor1
        self.altColor2 = altColor2
        self.tiles = {}
        self.surface = surface
        # 0 or 1 || 0 meaning white at the bottom side, 1 meaning black at the bottom side.
        self.rotation = rotation
        self.pieces = []
        self.square = {}
        self.directionoffsets = [8,-8,-1,1,7,-7,9,-9] # up, down, left, right, upleft, downright, upright, downleft
        self.numsquares_to_edge = self.pre_computed_move_data()

        self.color_to_move = "white"

        self.moves = []

    def change_color(self):
        if self.color_to_move == "white":
            self.color_to_move = "black"
        else:
            self.color_to_move = "white"

    # computes the number of squares to the edges at 8 direction
    def pre_computed_move_data(self):
        dict = {}
        for file in range(8):
            for rank in range(8):
                numNorth = 7 - rank
                numSouth = rank
                numWest = file
                numEast = 7 - file

                squareIndex = rank * 8 + file

                dict[squareIndex] = [
                    numNorth,  # up
                    numSouth,  # down
                    numWest,  # left
                    numEast,  # right
                    min(numNorth, numWest),  # top-left
                    min(numSouth, numEast),  # bottom-right
                    min(numNorth, numEast),  # top-right
                    min(numSouth, numWest),  # bottom-left
                ]
        return dict

    # Draws the tiles to the given surface with the colors of the Board.
    def generate_tiles(self):
        window_size = self.surface.get_size()  # size of the window
        self.tile_size = (
            window_size[0] / 8,
            window_size[1] / 8,
        )  # size of each square unit

        self.tiles = {}
        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 0:
                    color = self.color1
                else:
                    color = self.color2

                file = x if self.rotation == 0 else (7-x)
                rank = y if self.rotation == 1 else (7-y)
                square = (rank)*8 + (file)

                self.tiles[square] = [pygame.Rect(
                    x * self.tile_size[0], y * self.tile_size[1], self.tile_size[0], self.tile_size[1]), color, color]

    def draw_tiles(self):
        for tile in self.tiles.items():
            pygame.draw.rect(self.surface, tile[1][1], tile[1][0])

    def paint_square(self, squareNumber, color):
        self.tiles[squareNumber][1] = color

    def paint_moves(self, piece):
        for move in self.moves:
            if piece.square_index == move.startSquare:
                color = self.altColor1 if self.tiles[move.targetSquare][2] == self.color1 else self.altColor2
                self.paint_square(move.targetSquare, color)

    def reset_color(self):
        for tile in self.tiles.items():
            if tile[1][1] != tile[1][2]:
                tile[1][1] = tile[1][2]

    def set_square(self):
        self.square = {}
        for piece in self.pieces:
            self.square[piece.square_index] = piece

    # Dechypers the FEN code and adds each piece to the list after creating it.
    def init_pieces(self, starting_fen):
        rank = 8
        for r in starting_fen.split("/"):
            file = 1
            for p in r:
                # skips if `p` is a number
                if not p.isdecimal():
                    color = "black" if p.islower() else "white"

                    # creating the piece object
                    piece = Piece(
                        p.lower(),
                        color,
                        file,
                        rank,
                        1 + abs(800 - self.surface.get_width()) / 800,
                        self
                    )
                    self.square[(rank-1)*8 + (file - 1)] = piece
                    # adding the piece object to the pieces list
                    self.pieces.append(piece)
                file += 1
            rank -= 1

    def draw_pieces(self, pointer):
        for p in self.pieces:
            p.draw(self, pointer)

    def destroyPiece(self, piece):
        self.pieces.remove(piece)

    def MakeMove(self, x):
        move = self.GetMove(x)

        pieceToMove = self.square[move.startSquare] if move.startSquare in self.square.keys() else None
        targetPiece = self.square[move.targetSquare] if move.targetSquare in self.square.keys() else None

        pieceToMove.Move(move.targetSquare)
        if targetPiece != None:
            pieceToMove.Eat(targetPiece)
        
        print(move.isRook)
        if move.isRook:
            move.targetRook.Move(move.rookTargetSquare)


    def generate_moves(self):
        self.set_square()
        self.moves = []

        for i in range(64):
            # starting piece
            piece = self.square[i] if i in self.square.keys() else None

            if piece == None:
                continue

            # Only calculate the moves for color to move.
            if Piece.IsColour(piece, self.color_to_move):
                startSquare = piece.square_index

                if Piece.is_sliding(piece):
                    self.generate_sliding_moves(
                        startSquare, piece)  # Sliding pieces

                elif Piece.IsType(piece, "p"):  # Pawns
                    self.generate_pawn_moves(startSquare, piece)
                
                elif Piece.IsType(piece, "n"): # Knights
                    self.generate_knight_moves(startSquare, piece)

                elif Piece.IsType(piece, "k"):
                    self.generate_king_moves(startSquare, piece)

    def generate_sliding_moves(self, startSquare, piece):
        startDirIndex = 4 if Piece.IsType(piece, "b") else 0
        endDirIndex = 4 if Piece.IsType(piece, "r") else 8

        # calculate each direction
        for direction in range(startDirIndex, endDirIndex):
            for n in range(self.numsquares_to_edge[startSquare][direction]):

                targetSquare = startSquare +self.directionoffsets[direction]*(n+1)

                targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None

                # Blocked by friendly color
                if targetPiece != None:
                    if Piece.IsColour(piece, targetPiece.color):
                        break

                self.moves.append(Move(startSquare, targetSquare))

                if targetPiece != None:
                    # Blocked by opponent color
                    if not Piece.IsColour(piece, targetPiece.color):
                        break

    def generate_pawn_moves(self, startSquare, piece):

        # + direction if white, - direction if black
        direction = self.directionoffsets[0] if Piece.IsColour(piece, "white") else self.directionoffsets[1]
        
        range_ = 1
        if not piece.is_moved:
            range_ = 2 

        # Forward moves
        for n in range(range_):
            targetSquare = startSquare + direction*(n+1)
            
            targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None
            if targetPiece == None:
                self.moves.append(Move(startSquare,targetSquare))
            else:
                break
        
        # 39 - 48

        # Diagonal moves
        diagonals =[4,6] if Piece.IsColour(piece, "white") else [5,7]
        for direction in diagonals:
            # To avoid jumping from one edge to other
            if self.numsquares_to_edge[startSquare][direction] == 0:
                continue

            n = 1
            targetSquare = startSquare + self.directionoffsets[direction]*(n)

            targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None
            if targetPiece != None:
                if not Piece.IsColour(piece, targetPiece.color):
                    self.moves.append(Move(startSquare,targetSquare))
        # En Passant

    def generate_knight_moves(self, startSquare, piece):
        # Moves 1 right or 1 left then moves 2 up or 2 down (1) 
        # Moves 1 up or 1 down then moves 2 left or 2 right (2)

        # (1) 
        # Check 1 left and 1 right moves
        for direction in [2,3]:
            if self.numsquares_to_edge[startSquare][direction] < 1:
                continue
            
            targetSquareTemp = startSquare + self.directionoffsets[direction]

            # check up and down for corners and piece
            for direction in [0,1]:
                # Edge control
                if self.numsquares_to_edge[startSquare][direction] < 2:
                    continue

                targetSquare = targetSquareTemp + self.directionoffsets[direction]*2
                
                # Piece control
                targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None

                # Can't move on top of friendly piece
                if targetPiece != None:
                    if Piece.IsColour(piece, targetPiece.color):
                        continue

                self.moves.append(Move(startSquare, targetSquare))
        
        # (2)
        # Check 1 up and 1 down moves
        for direction in [0,1]:
            if self.numsquares_to_edge[startSquare][direction] < 1:
                continue
            
            targetSquareTemp = startSquare + self.directionoffsets[direction]

            # check up and down for corners and piece
            for direction in [2,3]:
                # Edge control
                if self.numsquares_to_edge[startSquare][direction] < 2:
                    continue

                targetSquare = targetSquareTemp + self.directionoffsets[direction]*2
                
                # Piece control
                targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None

                # Can't move on top of friendly piece
                if targetPiece != None:
                    if Piece.IsColour(piece, targetPiece.color):
                        continue

                self.moves.append(Move(startSquare, targetSquare))
        
    def generate_king_moves(self, startSquare, piece):
        # Goes 1 in all directions
        for direction in range(8):
            if self.numsquares_to_edge[startSquare][direction] < 1:
                continue
            
            targetSquare = startSquare + self.directionoffsets[direction]

            targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None
            if targetPiece != None:
                if Piece.IsColour(piece, targetPiece.color):
                    continue
            
            self.moves.append(Move(startSquare, targetSquare))

        # Check for left and right castle
        if not piece.is_moved:
            # check right [3]
            # Kingside castle
            directionIndex = 3
            for n in range(3):
                targetSquare = startSquare + self.directionoffsets[directionIndex]*(n+1)

                targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None
                if (targetPiece != None) and ((n+1) != 3):
                    break
                
                if targetPiece != None:
                    if Piece.IsType(targetPiece, "r") and not targetPiece.is_moved:
                        rookTarget = startSquare + self.directionoffsets[directionIndex]
                        self.moves.append(Move(startSquare, startSquare + self.directionoffsets[directionIndex]*2, isRook=True, targetRook=targetPiece, rookTargetSquare=rookTarget))

            # check left [2]
            # Queenside castle
            directionIndex = 2
            for n in range(4):
                targetSquare = startSquare + self.directionoffsets[directionIndex]*(n+1)

                targetPiece = self.square[targetSquare] if targetSquare in self.square.keys() else None
                if (targetPiece != None) and ((n+1) != 4):
                    break
                
                if targetPiece != None:
                    if Piece.IsType(targetPiece, "r") and not targetPiece.is_moved:
                        rookTarget = startSquare + self.directionoffsets[directionIndex]
                        self.moves.append(Move(startSquare, startSquare + self.directionoffsets[directionIndex]*2, isRook=True, targetRook=targetPiece, rookTargetSquare=rookTarget))

    # Find move from moves list to get all information
    def GetMove(self, x) -> Move:
        for move in self.moves:
            if x == move:
                return move
