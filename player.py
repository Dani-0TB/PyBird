import pygame, os

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Setup
        self.bird = pygame.image.load(os.path.join('Assets', 'bird.png')).convert_alpha()
        self.image = self.bird
        self.rect = self.image.get_rect(center = (100,400))

        # Movimiento
        self.GRAVITY = 0.25
        self.speed = 0

        #Animacion
        self.angle = 0

    def jump(self):
        self.angle = 0
        self.speed = -7
    
    def apply_gravity(self):
        if self.rect.bottom <= 700:
            self.speed += self.GRAVITY
            self.rect.y += self.speed
            self.falling = True
        if self.rect.top <= 0:
            self.rect.top = 0
    
    def animation_update(self):
        if self.speed > 0 and self.angle > -90:
            self.angle -= 3
        elif self.speed < 0 and self.angle < 45:
            self.angle += 3
        self.image = pygame.transform.rotate(self.bird, self.angle)


    def update(self):
        self.animation_update()
        self.apply_gravity()