import pygame


class Move:
    def __init__(self, startSquare, targetSquare, isRook=False, isEnPassant=False, targetPiece=None, targetPieceSquare=None, isMoved=False) -> None:
        self.startSquare = startSquare
        self.targetSquare = targetSquare

        self.isRook = isRook
        self.targetPiece = targetPiece
        self.targetPieceSquare = targetPieceSquare

        self.isMoved = isMoved

        self.isEnPassant = isEnPassant

    def __str__(self) -> str:
        return f"start: {self.startSquare}, target: {self.targetSquare}, isRook: {self.isRook}, isEnPassant: {self.isEnPassant}"

    def __eq__(self, __value: object) -> bool:
        if self.startSquare == __value.startSquare and self.targetSquare == __value.targetSquare:
            return True
        else:
            return False
