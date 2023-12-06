import pygame
import sys
import random
from settings import *
from abstract import *
from classes_base_flappy import *

class FlappyBird(Minigame_abs):
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

    def update_score(self):
            for pipe in self.pipes.sprites():
                if not pipe.passed and pipe.pipe_type == "bottom":
                    bird_rect = self.bird.sprite.rect
                    pipe_rect = pipe.rect
                    exit_position = pipe_rect.x + pipe_rect.width

                    if bird_rect.x > exit_position:
                        pipe.passed = True
                        self.score += 1

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
            self.update_score()

            self.pipes.update()
            self.ground.update()
        self.bird.update(user_input)

        # Check for collisions after updating the bird position
        self.collision_detector.check_collisions()
    
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
