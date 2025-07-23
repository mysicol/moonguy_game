import pygame
from src.moonguy import Moonguy

class Enemy(Moonguy):
    def __init__(self, screen, grass_height, x_pos):
        super().__init__(screen, grass_height, x_pos)

        self._sprite = pygame.image.load('src/images/enemy.png')
