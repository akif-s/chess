import pygame


class Sound:
    def __init__(self, path, volume=1.0) -> None:
        self.audio = pygame.mixer.Sound(f"audio/{path}")
        self.audio.set_volume(volume)  # maximum by default

    def Play(self):
        self.audio.play()

    def PlayCapture(volume=1.0):
        sound = pygame.mixer.Sound("audio/Capture.mp3")
        sound.set_volume(volume)
        sound.play()

    def PlayMove(volume=1.0):
        sound = pygame.mixer.Sound("audio/Move.mp3")
        sound.set_volume(volume)
        sound.play()
