import pygame

# Definindo as dimensões da tela do nosso jogo
screen_width = 1280
screen_height = 720

# Images

# Images for flappy bird
bird_images_flappy = [pygame.image.load("flappy_bird_assets/flappy_images/bird_down.png"),
               pygame.image.load("flappy_bird_assets/flappy_images/bird_mid.png"), 
               pygame.image.load("flappy_bird_assets/flappy_images/bird_up.png")]

skyline_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/background.png")
ground_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/ground.png") 
top_pipe_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/pipe_top.png")
bottom_pipe_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/pipe_bottom.png")
game_over_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/game_over.png")
start_image_flappy = pygame.image.load("flappy_bird_assets/flappy_images/start.png")

# Sounds for flappy
pygame.mixer.init()
die_sound_flappy = pygame.mixer.Sound("flappy_bird_assets/flappy_sounds/die.mp3")
score_sound_flappy = pygame.mixer.Sound("flappy_bird_assets/flappy_sounds/point.mp3")
flap_sound_flappy = pygame.mixer.Sound("flappy_bird_assets/flappy_sounds/flap.mp3")
hit_sound_flappy = pygame.mixer.Sound("flappy_bird_assets/flappy_sounds/hit.mp3")
transition_sound_flappy = pygame.mixer.Sound("flappy_bird_assets/flappy_sounds/transition.mp3")
