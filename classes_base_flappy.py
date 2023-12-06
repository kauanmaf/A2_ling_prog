import pygame
import sys
import random
from settings import *
from abstract import *

class Bird(Player):
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
    
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -screen_width:
            self.kill()  

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
