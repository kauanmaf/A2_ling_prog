import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)

# assets frog game
fg_background1 = pygame.image.load("./assets_frog/background1.png")
fg_background2 = pygame.image.load("./assets_frog/background2.png")
lilypad1 = pygame.image.load("./assets_frog/lilypad1.png")
lilypad2 = pygame.image.load("./assets_frog/lilypad2.png")
lilypad3 = pygame.image.load("./assets_frog/lilypad3.png")
alligator = pygame.image.load("./assets_frog/crocodile.png")
frog_img = pygame.image.load("./assets_frog/froginho.png")
death_box = pygame.image.load("./assets_frog/deathbox1.png")
dead_frog = pygame.image.load("./assets_frog/dead_frog'.png")

# first background image
fg_current_image = fg_background1

obstacle_images = [lilypad1, lilypad2, lilypad3, alligator]

# sound effects frog game
# soundtrack working
pygame.mixer.music.load("./assets_frog/a_frog_adventure.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# collision sound
fg_collision_sound = pygame.mixer.Sound("./assets_frog/wet_frog.mp3")
fg_collision_sound.set_volume(0.5)

# cores 
white = (255, 255, 255)

# frog game lane coordinates
left_lane = 480
center_lane = 640
right_lane = 800
lanes = [left_lane, center_lane, right_lane]

lane = random.choice(lanes)
image = random.choice(obstacle_images)

# frog starting coordinates
fg_player_x = 640
fg_player_y = 640


