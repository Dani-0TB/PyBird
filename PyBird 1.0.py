import pygame, os
from random import randint
from sys import exit
from player import Player
from pipes import Pipe
from trigger import Trigger

pygame.init()

# Seteo del juego
SCREEN_SIZE = WIDTH, HEIGHT = 500, 800
screen = pygame.display.set_mode(SCREEN_SIZE)
FPS = 120
clock = pygame.time.Clock()
pygame.display.set_caption("PyBird - A python Flappy Bird Clone")
icon_surf = pygame.image.load(os.path.join('Assets', 'bird.png'))
pygame.display.set_icon(icon_surf)
pygame.mixer.init()

# Fuentea
font_px = 75
font = pygame.font.Font(os.path.join("Assets", "font.ttf"), font_px)
font2 = pygame.font.Font(os.path.join("Assets", "font2.ttf"), font_px)


# Background
bg_surf = pygame.image.load(os.path.join('Assets', 'ground.png')).convert_alpha()
bg_rect = bg_surf.get_rect(topleft = (0,700))

bg2_surf = pygame.image.load(os.path.join('Assets', 'bg.png')).convert()
bg2_rect = bg2_surf.get_rect(topleft = (0,0))

# Sonidos
hit = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))
fall = pygame.mixer.Sound(os.path.join('Assets', 'fall.wav'))
flap = pygame.mixer.Sound(os.path.join('Assets', 'flap.wav'))
Oneup = pygame.mixer.Sound(os.path.join('Assets', '1up.wav'))

# Función principal
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
    
    # Seteo de escenas
    spawn_pipes = False
    game = False
    game_starting = True
    final_screen = False
    animation_counter = FPS*4
    
    # Main loop
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
                if event.key == pygame.K_SPACE and game:
                        player.sprite.jump()
                        flap.play()
                        
                if event.key == pygame.K_SPACE and final_screen:
                    player.sprite.rect.center = (100,250)
                    player.sprite.speed = 0
                    player.sprite.angle = 0
                    score = 0
                    player.update()
                    pipes.empty()
                    triggers.empty()
                    game_starting = True
                    final_screen = False
                           
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0] and game:
                    flap.play()
                    player.sprite.jump()
                if mouse[2] and final_screen:
                    player.sprite.rect.center = (100,250)
                    player.sprite.speed = 0
                    player.sprite.angle = 0
                    player.update()
                    score = 0
                    pipes.empty()
                    triggers.empty()
                    game_starting = True
                    final_screen = False
                    
            # Spawn pipes                    
            if event.type == pipe_spawn and spawn_pipes:
                    pos = randint(100,400)
                    pipes.add(Pipe(False,pos))
                    pipes.add(Pipe(True,pos))
                    triggers.add(Trigger(pos))
            
        # Game loops
        if game_starting:
            player.sprite.rect.center = (100, 250)
            font = pygame.font.Font(os.path.join("Assets", "font.ttf"), 30)
            font2 = pygame.font.Font(os.path.join("Assets", "font2.ttf"), 30)
            
            spawn_pipes = False
            if animation_counter >= 0:
                
                
                font_surface = pygame.Surface((100,30))
                
                background_text = font2.render("Get Ready", True, (225,225,225))
                score_text = font.render("Get Ready", True, (0,0,0))
                font_rect = font_surface.get_rect(center = (225, 500))
                font_rect2 = font_surface.get_rect(center = (226, 501))
                
        
                move_background(bg_rect, bg2_rect)

                screen.blit(bg2_surf, bg2_rect)
                screen.blit(bg_surf,bg_rect)
                player.draw(screen)
                screen.blit(background_text, font_rect2)
                screen.blit(score_text, font_rect)
                
                animation_counter -= 1
                
            elif animation_counter <= 0:
                animation_counter = 2*FPS
                game_starting = False
                game = True

                        
        if game:
            if not spawn_pipes:
                pygame.time.set_timer(pipe_spawn,1500)
                spawn_pipes = True
            font = pygame.font.Font(os.path.join("Assets", "font.ttf"), font_px)
            font2 = pygame.font.Font(os.path.join("Assets", "font2.ttf"), font_px)
            font_surface = pygame.Surface((60,font_px))
            background_text = font2.render(f"{score}", True, (225,225,225))
            score_text = font.render(f"{score}", True, (0,0,0))
            font_rect = font_surface.get_rect(center = (260, 100))
            font_rect2 = font_surface.get_rect(center = (260 +1, 103))
            pipes.update()
            triggers.update()
            triggers.draw(screen)
            # Game Logic
            if player.sprite.rect.bottom >= 700:
                player.sprite.hit_ground(15)
                game = False
                final_screen = True
                hit.play()
            for pipe in pipes:
                if pipe.rect.colliderect(player.sprite.rect):
                    hit.play()
                    fall.play()
                    player.sprite.jump()
                    game = False
                    final_screen = True
            for trigger in triggers:
                if trigger.rect.colliderect(player.sprite.rect) and not trigger.triggered:
                    score += 1
                    Oneup.play()
                    trigger.triggered = True

            move_background(bg_rect, bg2_rect)
        # Draw Screen
            screen.blit(bg2_surf, bg2_rect)
            pipes.draw(screen)
            screen.blit(bg_surf,bg_rect)
            player.update()
            player.draw(screen)
            screen.blit(background_text, font_rect2)
            screen.blit(score_text, font_rect)

        if final_screen:
            screen.blit(bg2_surf, bg2_rect)
            pipes.draw(screen)
            screen.blit(bg_surf,bg_rect)
            player.update()
            player.draw(screen)
            screen.blit(background_text, font_rect2)
            screen.blit(score_text, font_rect)

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
