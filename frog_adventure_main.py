from settings import *
import pygame
from classes_base_frog import *
from pygame.locals import *

class FrogJourneyGame:
    
    def __init__(self):

        self.player = Player1(frog_img, fg_player_x, fg_player_y, speed = 6)
        self.player_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.collision_detection = CollisionDetection()
        self.background_and_score = BackgroundAndScore()

        # Add the player to the player_group
        self.player_group.add(self.player)

        # Initialize game variables
        self.fg_target_lane = fg_player_x
        self.fg_gameover = False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(fps)
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                self.fg_gameover = True

            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.player.rect.center[0] > left_lane:
                    self.fg_target_lane = left_lane
                elif event.key == K_RIGHT and self.player.rect.center[0] < right_lane:
                    self.fg_target_lane = right_lane

    def update(self):
        self.move_player()
        self.spawn_obstacles()
        self.move_obstacles()
        self.check_collisions()

    def move_player(self):
        if self.player.rect.center[0] < self.fg_target_lane:
            self.player.rect.x += self.player.speed
            if self.player.rect.center[0] > self.fg_target_lane:
                self.player.rect.center = (self.fg_target_lane, self.player.rect.centery)
        elif self.player.rect.center[0] > self.fg_target_lane:
            self.player.rect.x -= self.player.speed
            if self.player.rect.center[0] < self.fg_target_lane:
                self.player.rect.center = (self.fg_target_lane, self.player.rect.centery)

    def spawn_obstacles(self):
        if len(self.obstacle_group) < 2:
            add_obstacle = True
            for obstacle in self.obstacle_group:
                if obstacle.rect.top < obstacle.rect.height * 1.5:
                    add_obstacle = False

            if add_obstacle:
                lane = random.choice(lanes)
                image = random.choice(obstacle_images)
                obstacle = Obstacle(image, lane, screen_height / -2)
                self.obstacle_group.add(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacle_group:
            obstacle.rect.y += fg_speed
            if obstacle.rect.top >= screen_height:
                obstacle.kill()
                self.background_and_score.update_score()

    def check_collisions(self):
        if self.collision_detection.check(self.player, self.obstacle_group):
            fg_collision_sound.play()
            self.fg_gameover = True
            self.player.set_dead()

    def render(self):
        screen.fill((0, 0, 0))

        self.background_and_score.draw_background(screen)

        if self.player.visible:
            self.player_group.draw(screen)

        self.obstacle_group.draw(screen)

        self.background_and_score.draw_score(screen)

        if self.fg_gameover:
            screen.blit(death_box, (0, 0))

        pygame.display.update()

        while self.fg_gameover:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.fg_gameover = False

                if event.type == KEYDOWN:
                    if event.key == K_y:
                        self.reset_game()

                    elif event.key == K_n:
                        pygame.quit()
                        quit()

    def reset_game(self):
        self.fg_gameover = False
        self.fg_speed = 2
        self.background_and_score.fg_score = 0
        self.obstacle_group.empty()
        self.player.rect.center = [fg_player_x, fg_player_y]
        self.player.visible = True
        self.player.set_alive()

if __name__ == "__main__":
    game = FrogJourneyGame()
    game.run()