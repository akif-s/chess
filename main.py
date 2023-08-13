import pygame
from pygame.locals import *
import sys
from board import Board
from mouse import Pointer

pygame.init()

WINDOW_SIZE = (1200, 1200)

screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board((233, 217, 185), (170, 137, 105), (219, 116, 116),
              (179, 86, 86), screen, rotation=0)

mouse=Pointer(board.rotation, screen)
2
startingFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

board.init_pieces(startingFen)
board.generate_tiles()

while True:
    board.draw_tiles()
    board.draw_pieces(mouse)

    if mouse.piece != None:
        board.paint_moves(mouse.piece)
    else:
        board.reset_color()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if event.key == K_LEFT:
                if len(board.madeMoves) > 0:
                    board.UnMakeMove(len(board.madeMoves) - 1)

        if event.type == MOUSEMOTION:
            mouse.update_pos(event.pos)

        if event.type == MOUSEBUTTONDOWN:
            mouse.press=True
            mouse.pos0=mouse.pos

            if mouse.piece == None:
                mouse.grab_piece(board.pieces, board)

        if event.type == MOUSEBUTTONUP:
            if mouse.piece != None:
                mouse.release_piece(board)

            mouse.drag=False
            mouse.press=False

    pygame.display.update()
