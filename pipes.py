import pygame, os
from random import randint


class Pipe(pygame.sprite.Sprite):
    def __init__(self, is_bottom, y_pos):
        super().__init__()
        # Pipe parameters
        self.is_bottom = is_bottom
        self.x_pos = 700
        self.y_pos = y_pos
        self.speed = 2
        # Pipe Sprite
        self.image = pygame.image.load(os.path.join('Assets', 'pipe.png')).convert_alpha()
        if self.is_bottom:
            self.y_pos += 180
            self.rect = self.image.get_rect(midtop = (self.x_pos, self.y_pos))
        else:
            self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))
        

    def move_pipe(self):
        self.rect.x -= self.speed
        if self.rect.left <= -200:
             self.kill()

    def update(self):
        self.move_pipe()
        