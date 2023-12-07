import pygame
from pygame.locals import *
import random

pygame.init()

screen_width = 1280
screen_height = 720

# assets frog game
fg_background1 = pygame.image.load("./assets/background1.png")
fg_background2 = pygame.image.load("./assets/background2.png")
lilypad1 = pygame.image.load("./assets/lilypad1.png")
lilypad2 = pygame.image.load("./assets/lilypad2.png")
lilypad3 = pygame.image.load("./assets/lilypad3.png")
alligator = pygame.image.load("./assets/crocodile.png")
frog_img = pygame.image.load("./assets/froginho.png")
death_box = pygame.image.load("./assets/deathbox1.png")
dead_frog = pygame.image.load("./assets/dead_frog'.png")

#first background image
fg_current_image = fg_background1

#sound effects frog game

#soundtrack working
pygame.mixer.music.load("./assets/a_frog_adventure.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#collision sound
fg_collision_sound = pygame.mixer.Sound("./assets/wet_frog.mp3")
fg_collision_sound.set_volume(0.5)

# colors
white = (255, 255, 255)

# lane coordinates
left_lane = 480
center_lane = 640
right_lane = 800
lanes = [left_lane, center_lane, right_lane]

# player's starting coordinates
fg_player_x = center_lane
fg_player_y = 640

fg_target_lane = center_lane

# frame settings
clock = pygame.time.Clock()
fps = 100

# game settings
fg_gameover = False
fg_speed = 2
fg_score = 0