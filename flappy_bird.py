from typing import Any
import pygame
import sys
import random
from settings import *
from abstract import *

# screen = pygame.display.set_mode((screen_width, screen_height))


class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_start_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position 
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True
        self.bird_start_position = bird_start_position
        self.y_pos_ground = 530


    def update(self, user_input):
        # Animating bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10] 

        self.vel += 0.5
        if self.vel >7:
            self.vel = 7
        if self.rect.bottom < self.y_pos_ground:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = 0
        
        # mudnado o jeito que o passaro olha
        self.image = pygame.transform.rotate(self.image, self.vel*-7)

        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7

class Ground(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, scroll_speed) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.scroll_speed = scroll_speed
    
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -self.image.get_width():
            self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, pipe_type, scroll_speed, bird_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.scroll_speed = scroll_speed
        self.bird_position = bird_position

        # Adding score related variables
        self.enter = False
        self.exit = False
        self.passed = False

        self.pipe_type = pipe_type
        self.score = 0

    
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()
        
        if self.pipe_type == "bottom":
            if self.bird_position[0]> self.rect.topleft[0] and not self.passed:
                self.enter = True
            if self.bird_position[0]> self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                self.score += 1
    
    def get_score(self):
        return self.score

class CollisionDetector:
    def __init__(self, bird, ground, pipes, screen):
        self.bird = bird
        self.ground = ground
        self.pipes = pipes
        self.screen = screen

    def check_collisions(self):
        collision_ground = pygame.sprite.spritecollide(self.bird.sprite, self.ground, False)
        collision_pipes = pygame.sprite.spritecollide(self.bird.sprite, self.pipes, False)

        if collision_pipes or collision_ground:
            self.bird.sprite.alive = False
            if collision_ground:
                # Draw the game over image
                self.screen.blit(game_over_image,
                            (screen_width // 2 - game_over_image.get_width() // 2,
                             screen_height // 2 - game_over_image.get_height() // 2))

class Menu:
    def __init__(self, screen, bird_start_position):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bird_start_position = bird_start_position

    def draw(self):
        self.screen.blit(skyline_image, (0, 0))
        self.screen.blit(ground_image, Ground(0, 520, 3))
        self.screen.blit(ground_image, Ground(ground_image.get_width(), 520, 3))

        self.screen.blit(bird_images[0], self.bird_start_position)
        self.screen.blit(start_image, (screen_width // 2 - start_image.get_width() // 2,
                                        screen_height // 2 - start_image.get_height() // 2))


class FlappyBird:
    def __init__(self, screen):
        self.screen = screen
        self.scroll_speed = 3
        self.bird_position = (200, screen_height / 2 -100)

        self.bird = pygame.sprite.GroupSingle()
        self.pipes = pygame.sprite.Group()
        self.ground = self.create_ground()
        self.create_bird()

        self.collision_detector = CollisionDetector(self.bird, self.ground, self.pipes, self.screen)

        self.score = 0
        self.pipe_timer = 100

        self.screen = screen
        self.menu = Menu(self.screen, self.bird_position)
        self.game_started = False

        self.start_delay_duration = 15  # Set the delay duration (in frames)
        self.current_delay = self.start_delay_duration


    def create_bird(self):
        self.bird.add(Bird(self.bird_position))

    def create_ground(self):
        x_pos_ground = 0
        y_pos_ground = 530
        ground_group = pygame.sprite.Group()  # Create a group to hold grounds
        ground_group.add(Ground(x_pos_ground, y_pos_ground, self.scroll_speed))
        ground_group.add(Ground(x_pos_ground + ground_image.get_width(), y_pos_ground, self.scroll_speed))
        ground_group.add(Ground(x_pos_ground + 2 * ground_image.get_width(), y_pos_ground, self.scroll_speed))
        return ground_group  

    def spawn_pipes(self):
        if self.pipe_timer <= 0 and self.bird.sprite.alive:
            x_top = 1300
            x_bottom = 1300

            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()

            self.pipes.add(
                Pipe(x_top, y_top, top_pipe_image, "top", self.scroll_speed, self.bird.sprite.rect.topleft))
            self.pipes.add(
                Pipe(x_bottom, y_bottom, bottom_pipe_image, "bottom", self.scroll_speed, self.bird.sprite.rect.topleft))

            self.pipe_timer = 100

        self.pipe_timer -= 1

    def draw(self):

        # Drawing background
        self.screen.blit(skyline_image, (0, 0))

        # Drawing the pipes
        self.pipes.draw(self.screen)

        # Drawing the grounds
        self.ground.draw(self.screen)
        self.bird.draw(self.screen)

        # Spawning pipes
        self.spawn_pipes()

        # Render the score text
        score_text = pygame.font.Font(None, 36).render(f"Score: {self.score}", True, pygame.Color(255, 255, 255))
        self.screen.blit(score_text, (20, 20))

    def update(self):
        user_input = pygame.key.get_pressed()

        if len(self.ground) <= 2:
            self.ground = self.create_ground()  

        if self.bird.sprite.alive:
            self.pipes.update()
            self.ground.update() 
        self.bird.update(user_input)
        
        self.collision_detector.check_collisions()

    def reset_game(self):
        # Reset game state for a new game
        self.bird_position = (200, screen_height / 2 - 100)
        self.create_bird()
        self.pipes.empty()
        self.ground.empty()
        self.ground = self.create_ground()
        self.score = 0
        self.pipe_timer = 100
        self.game_over = False
        self.current_restart_delay = self.start_delay_duration
        self.bird.sprite.alive = True  # Ensure the bird is alive for the new game

        self.collision_detector = CollisionDetector(self.bird, self.ground, self.pipes, self.screen)


    def run(self): 
        keys = pygame.key.get_pressed()

        if not self.game_started:
            self.menu.draw()

            if keys[pygame.K_SPACE]:
                self.current_delay -= 1
            else:
                self.current_delay = self.start_delay_duration

            if self.current_delay <= 0:
                self.game_started = True
                self.current_delay = self.start_delay_duration
        
        elif not self.bird.sprite.alive and keys[pygame.K_r] :
            self.reset_game()

        else:
            self.draw()
            self.update()

# Configurando o jogo
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = FlappyBird(screen)

# Adicionando nome
pygame.display.set_caption("Mini Arcade")

# making the loop while to start
while True:
    # Configurando a taxa de atualização do jogo
    clock.tick(100)

    # Configurando o fundo da tela
    screen.fill((0, 0, 0))

    # Criando uma instância do jogo
    game.run()

    # Loop for para casa a pessoa queira sair do jogo
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Fazendo um update pra manter no caso de atualizações
    pygame.display.update()