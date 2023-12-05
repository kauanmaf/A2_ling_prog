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
    def __init__(self, bird, ground, pipes):
        self.bird = bird
        self.ground = ground
        self.pipes = pipes

    def check_collisions(self):
        collision_ground = pygame.sprite.spritecollide(self.bird.sprite, self.ground, False)
        collision_pipes = pygame.sprite.spritecollide(self.bird.sprite, self.pipes, False)

        if collision_pipes or collision_ground:
            self.bird.sprite.alive = False
            if collision_ground:
                # Draw the game over image
                screen.blit(game_over_image,
                            (screen_width // 2 - game_over_image.get_width() // 2,
                             screen_height // 2 - game_over_image.get_height() // 2))


class FlappyBird:
    def __init__(self, screen):
        self.screen = screen
        self.scroll_speed = 3
        self.bird_position = (200, screen_height / 2)

        self.bird = pygame.sprite.GroupSingle()
        self.pipes = pygame.sprite.Group()
        self.ground = self.create_ground()
        self.create_bird()

        self.collision_detector = CollisionDetector(self.bird, self.ground, self.pipes)

        self.score = 0
        self.pipe_timer = 100


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


    def run(self):
        self.draw()
        self.update()


import pygame
from settings import *
from abstract import Minigame_abs
from flappy_bird import FlappyBird


class Minigame():
    def __init__(self, current_level, surface, create_level_map):
        # level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = minijogos_lista[current_level]
        level_content = level_data["content"]
        self.new_max_level = level_data["unlock"]
        self.create_level_map = create_level_map
        
        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surf = self.font.render(level_content, True, "White")
        self.text_rect = self.text_surf.get_rect(center=(screen_width/2, screen_height/2))

    def run_minigame(self):
    
        if int(self.current_level) == 0:
            return FlappyBird(self.display_surface)
        
        elif self.current_level == 1:
            # Run SPACE_INVADERS minigame
            print("Running SPACE_INVADERS minigame")
        elif self.current_level == 2:
            # Run PAC_MAN minigame
            print("Running PAC_MAN minigame")
        elif self.current_level == 3:
            # Run FLAPPY_BIRD minigame
            print("Running FLAPPY_BIRD minigame")

import pygame
from settings import minijogos_lista

class Node(pygame.sprite.Sprite):
    "Classe necessária para a definição dos retângulos de cada bloco do jogo"
    def __init__(self, pos, status, icon_speed):
        """Classe que inicializa os Nodos
        TODO: colocar param, colocar imagens
        """
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == "available":
            self.image.fill("red")
        else: 
            self.image.fill("grey")

        self.rect = self.image.get_rect(center=pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2), self.rect.centery - (icon_speed/2),icon_speed,icon_speed)

class Icon(pygame.sprite.Sprite):
    """
    Classe reponsável por criar o personagem que se movimenta pelos minimaps
    TODO: Colocar param, colocar imagem
    """

    def __init__(self,pos):
        """Classe que inicializa o Icon que fica entre os minijogos
        TODO: colocar param, colocar imagens
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.center = self.pos

class Level_map():
    def __init__(self, start_level, max_level, surface, create_level_map):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level_map = create_level_map

        # movement logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        # sprites
        self.create_nodes()
        self.setup_icon()

    def create_nodes(self):
        self.nodes = pygame.sprite.Group() 

        for index, node_data in enumerate(minijogos_lista.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["posicao"], "available", self.speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data["posicao"], "locked", self.speed)
            self.nodes.add(node_sprite)
    
    def draw_paths(self):
        centers = []
        for index, node_data in enumerate(minijogos_lista.values()):
            if index <= self.max_level:
                centers.append(node_data["posicao"])

        if 1 <= len(centers):
            pygame.draw.lines(self.display_surface, "red", False, centers, 6)
    
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        if not self.moving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data("next")
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level != 0:
                self.move_direction = self.get_movement_data("previous")
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level_map(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == "next":
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()
    
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

import sys
import pygame
from settings import *
from level_map import Level_map
from minigame import *

screen = pygame.display.set_mode((screen_width, screen_height))

class Game:
    """
    Classe responsável por gerenciar a instância do jogo.

    :ivar int max_level: O nível máximo permitido no jogo.
    :ivar Level_map level_map: A instância do mapa de níveis.
    :ivar str status: O status atual do jogo ('level_map' ou 'minigame').

    :param int max_level: O nível máximo padrão ao inicializar o jogo.
    """
    def __init__(self, max_level=3):
        """
        Inicializa uma nova instância do jogo.

        :param int max_level: O nível máximo permitido no jogo.
        """

        self.max_level = max_level

        # Passamos a função create_minigame dentro de level_map para chama-la dentro de level_map e instanciar um jogo.
        self.level_map = Level_map(0, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def create_minigame(self, current_level):
        """
        Cria uma nova instância de Minigame.

        :param current_level: O nível atual para o Minigame.
        :type current_level: int

        :return: A instância do Minigame criada.
        :rtype: Minigame
        """
        self.minigame = Minigame(current_level, screen, self.level_map)
        self.status = "minigame"

    def create_level_map(self, current_level, new_max_level):
        """
        Cria uma nova instância de Level_map.

        :param current_level: O nível atual para o novo Level_map (int).
        :type current_level: int

        :param new_max_level: O novo nível máximo (int).
        :type new_max_level: int

        :return: A instância do novo Level_map criada.
        :rtype: Level_map
        """
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.level_map = Level_map(current_level, self.max_level, screen, self.create_minigame)
        self.status = "level_map"

    def run(self):
        """
        Executa o loop do jogo com base no status atual.
        """
        if self.status == "level_map":
            self.level_map.run()
        else:
            self.minigame.run_minigame()

import sys
import pygame
from settings import *
from Game import *

# Configurando o jogo 
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

# Adicionando nome 
pygame.display.set_caption("Mini Arcade")


# making the loop while to start
while True:
    # Configurando a taxa de atualização do jogo 
    clock.tick(100) 

    # Configurando o fundo da tela
    screen.fill((0,0,0))

    # Criando uma instância do jogo 
    game.run()

    # Loop for para casa a pessoa queira sair do jogo 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fazendo um update pra manter no caso de atualizações
    pygame.display.update()