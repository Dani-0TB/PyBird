import pygame

class Trigger(pygame.sprite.Sprite):
    def __init__(self,y_pos):
        super().__init__()
        self.y_pos = y_pos
        self.image = pygame.Surface((1, 200))
        self.rect = self.image.get_rect(x = 790, top = y_pos)
        self.speed = 2
        self.triggered = False
        
    def move_surface(self):
        self.rect.x -= self.speed
        if self.rect.x <= -100: self.kill()

    def update(self):
        self.move_surface()