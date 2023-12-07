import pygame
from pygame.locals import *
import random


pygame.init()

background1 = pygame.image.load("./assets/background1.png")
background2 = pygame.image.load("./assets/background2.png")
lilypad1 = pygame.image.load("./assets/lilypad1.png")
lilypad2 = pygame.image.load("./assets/lilypad2.png")
lilypad3 = pygame.image.load("./assets/lilypad3.png")
alligator = pygame.image.load("./assets/crocodile.png")
frog_img = pygame.image.load("./assets/froginho.png")
death_box = pygame.image.load("./assets/deathbox1.png")
dead_frog = pygame.image.load("./assets/dead_frog'.png")


dead_frog_rect = dead_frog.get_rect()

pygame.mixer.music.load("./assets/a_frog_adventure.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

collision_sound = pygame.mixer.Sound("./assets/wet_frog.mp3")
collision_sound.set_volume(0.5)

current_image = background1

width = 1280
height = 720
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('A Frog Journey')


# colors
white = (255, 255, 255)

# lane coordinates
left_lane = 480
center_lane = 640
right_lane = 800
lanes = [left_lane, center_lane, right_lane]

# player's starting coordinates
player_x = center_lane
player_y = 640

target_lane = center_lane

# frame settings
clock = pygame.time.Clock()
fps = 100

# game settings
gameover = False
speed = 2
score = 0

class Objects(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerObject(Objects):
    
    def __init__(self, x, y, speed):
        super().__init__(frog_img, x, y)
        self.visible = True
        self.is_dead = False  # New property to track player state
        self.speed = 6

    def set_dead(self):
        self.is_dead = True
        self.image = dead_frog  # Change the player's image to dead_frog
        self.rect = self.image.get_rect()
        self.speed = 3

    def set_alive(self):
        self.is_dead = False
        self.image = frog_img  # Change the player's image back to frog_img
        self.rect = self.image.get_rect()

# sprite groups
player_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# create the player's frog
player = PlayerObject(player_x, player_y, speed=6)
player_group.add(player)

# load the obstacle images
obstacle_images = [lilypad1, lilypad2, lilypad3, alligator]

# game loop
running = True
while running:
    
    clock.tick(fps)
    
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.music.stop()  
            running = False
            
        # move the frog using the left/right arrow key
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                target_lane = left_lane
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                target_lane = right_lane
    
    # Smoothly move the frog towards the target lane
    if player.rect.center[0] < target_lane:
        player.rect.x += player.speed
        if player.rect.center[0] > target_lane:
            player.rect.center = (target_lane, player.rect.centery)
    elif player.rect.center[0] > target_lane:
        player.rect.x -= player.speed
        if player.rect.center[0] < target_lane:
            player.rect.center = (target_lane, player.rect.centery)
    
                    
    # Draw the current image on the screen
    if pygame.time.get_ticks() % 2000 < 1000:
        background_image = background1
    else:
        background_image = background2

    screen.blit(background_image, (0, 0))


    if player.visible:
        player_group.draw(screen)
    
    # add a obstacle
    if len(obstacle_group) < 2:
        
        # ensure there's enough gap between vehicles
        add_obstacle = True
        for obstacle in obstacle_group:
            if obstacle.rect.top < obstacle.rect.height * 1.5:
                add_obstacle = False
                
        if add_obstacle:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random obstacle image
            image = random.choice(obstacle_images)
            vehicle = Objects(image, lane, height / -2)
            obstacle_group.add(vehicle)
    
    # make the obstacles move
    for obstacle in obstacle_group:
        obstacle.rect.y += speed
        
        # remove obstacle once it goes off screen
        if obstacle.rect.top >= height:
            obstacle.kill()
            
            # add to score
            score += 1
            
            # speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1
    
    
    # draw the obstacles
    obstacle_group.draw(screen)
    
    # display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (640, 40)
    screen.blit(text, text_rect)
    
    # check if there's a head on collision
    if pygame.sprite.spritecollide(player, obstacle_group, True):
        
        collision_sound.play()
        gameover = True

        player.set_dead() 
        
            
    # display game over
    if gameover:
        
        screen.blit(death_box, (0, 0))

    pygame.display.update()

    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    obstacle_group.empty()
                    player.rect.center = [player_x, player_y]
                    player.visible = True

                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

    pygame.display.update()

pygame.quit()