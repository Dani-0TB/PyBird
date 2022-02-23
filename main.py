import pygame, os
from random import randint
from sys import exit
from player import Player
from pipes import Pipe
from trigger import Trigger

# Seteo del juego
SCREEN_SIZE = WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode(SCREEN_SIZE)
FPS = 120
clock = pygame.time.Clock()
pygame.display.set_caption("PyBird - A python Flappy Bird Clone")
icon_surf = pygame.image.load(os.path.join('Assets', 'bird.png'))
pygame.display.set_icon(icon_surf)
pygame.mixer.init()

# Background
bg_surf = pygame.image.load(os.path.join('Assets', 'ground.png')).convert_alpha()
bg_rect = bg_surf.get_rect(topleft = (0,700))

bg2_surf = pygame.image.load(os.path.join('Assets', 'bg.png')).convert()
bg2_rect = bg2_surf.get_rect(topleft = (0,0))

# Sounds
hit = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))
fall = pygame.mixer.Sound(os.path.join('Assets', 'fall.wav'))
flap = pygame.mixer.Sound(os.path.join('Assets', 'flap.wav'))
Oneup = pygame.mixer.Sound(os.path.join('Assets', '1up.wav'))

# función principal
def main():
    score = 0
    # Seteo del player
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    # Seteo de obstaculos
    pipes = pygame.sprite.Group()
    triggers = pygame.sprite.Group()

    # Timers
    pipe_spawn = pygame.USEREVENT+1
    pygame.time.set_timer(pipe_spawn,1500)
    
    score_colliding = False
    game_on = True
    menu = False
    final_screen = False

    while True:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Controls   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE and game_on:
                        player.sprite.jump()
                        flap.play()
                if event.key == pygame.K_r and not game_on:
                    player.sprite.rect.center = (100,250)
                    player.sprite.speed = 0
                    player.sprite.angle = 0
                    pipes.empty()
                    game_on = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0] and game_on:
                    flap.play()
                    player.sprite.jump()
                if mouse[2] and not game_on:
                    player.sprite.rect.center = (100,250)
                    player.sprite.speed = 0
                    player.sprite.angle = 0
                    pipes.empty()
                    game_on = True
                    
            # Spawn pipes
            if event.type == pipe_spawn:
                pos = randint(100,400)
                pipes.add(Pipe(False,pos))
                pipes.add(Pipe(True,pos))
                triggers.add(Trigger(pos))
        # Game loops
        if game_on:
            pipes.update()
            triggers.update()
            triggers.draw(screen)
            # Game Logic
            if player.sprite.rect.bottom >= 700:
                game_on = False
                hit.play()
            for pipe in pipes:
                if pipe.rect.colliderect(player.sprite.rect):
                    hit.play()
                    fall.play()
                    player.sprite.jump()
                    game_on = False
            for trigger in triggers:
                if trigger.rect.colliderect(player.sprite.rect):
                    score += 1
                    Oneup.play()

            move_background(bg_rect, bg2_rect)
        # Draw Screen
        screen.blit(bg2_surf, bg2_rect)
        pipes.draw(screen)
        
        screen.blit(bg_surf,bg_rect)
        player.update()
        player.draw(screen)
        
        pygame.display.update()
        clock.tick(FPS)


def move_background(background, background2):
    background.left -= 2
    if background.left < -50:
        background.left = 0

    background2.left -= 1
    if background2.left < -952:
        background2.left = 0


if __name__ == "__main__":
    main()