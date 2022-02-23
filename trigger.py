import pygame

class Trigger(pygame.sprite.Sprite):
    def __init__(self,y_pos):
        super().__init__()
        self.y_pos = y_pos
        self.image = pygame.Surface((10, 180))
        self.image.fill('Blue')
        self.rect = self.image.get_rect(x = 600, top = y_pos)
        self.speed = 2
    def move_surface(self):
        self.rect.x -= self.speed
        self.kill()

    def update(self):
        self.move_surface()