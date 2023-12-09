from settings_frog import *
import pygame
from classes_base_frog import *
from pygame.locals import *
from abstract import Minigame_abs
import sys

class FrogJourneyGame(Minigame_abs):
    """
    Uma classe representando o jogo Frog Adventure
    
    Atributos:
    ----------
    - ``__player`` (Player1):
        Instância da classe Player1.

    - ``__collision_detection`` (CollisionDetection):
        Instância da classe CollisionDetection.

    - ``__score`` (Score):
        Instância da classe Score.

    - ``__background`` (Background):
        Instância da classe Background.

    - ``__player_group`` (pygame.sprite.Group):
        Grupo que contém o sprite do player.

    - ``__obstacle_group`` (pygame.sprite.Group):
        Grupo de contém os sprites dos objetos.

    - ``__fg_target_lane`` (int):
        coordenada da lane para movimentação do player.

    - ``__fg_gameover`` (bool):
        Utilizada para ações quando o player perde.

    - ``__fg_speed`` (int):
        Velocidade dos obstáculos.

    - ``__clock`` (pygame.time):
        método para controle dos ticks.

    - ``__running`` (bool):
        Variável que será True caso o jogo esteje rodando.
        
    Métodos:
    --------
    - ``run(self)``:
        Essa função abriga o loop que roda o jogo.

    - ``handle_events(self)``:
        Essa função controla os eventos de fechamento do jogo e aperto de teclas.    

    - ``update(self)``:
        Função que atualiza os aspectos do jogo a cada quadro.   

    - ``move_player(self)``:
        Função que define as características de movimentação do player.   

    - ``draw_obstacles(self)``:
        Função que desenha os obstáculos do jogo.

    - ``move_obstacles(self)``:
        Função que garante a movimentação dos obstáculos.

    - ``check_collisions(self)``:
        Função que detecta colisões e realiza ações a respeito.

    - ``render(self)``:
        Função que renderiza o jogo.

    - ``reset_game(self)``:
        Função que define aspectos do jogo ao ser resetado
    """
    def __init__(self):
        """Essa função inicializa as classes importadas e cria variáveis necessárias 
        para o funcionamento do jogo
        """
        self.__player = Player1()
        self.__collision_detection = CollisionDetection()
        self.__background = Background()
        self.__score = Score()

        self.__player_group = pygame.sprite.Group()
        self.__obstacle_group = pygame.sprite.Group()

        self.__player_group.add(self.__player)

        self.__fg_target_lane = fg_player_x
        self.__fg_gameover = False
        self.__fg_speed = 2

        self.__clock = pygame.time.Clock()
        self.__running = True
        
    def run(self):
        """Essa função abriga o loop que roda o jogo
        """
        while self.__running:
            self.__clock.tick(100)
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        """Essa função controla os eventos de fechamento do jogo e aperto de teclas
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.__player.rect.center[0] > left_lane:
                    self.__fg_target_lane = left_lane
                elif event.key == K_RIGHT and self.__player.rect.center[0] < right_lane:
                    self.__fg_target_lane = right_lane

    def update(self):
        """Função que atualiza os aspectos do jogo a cada quadro.
        """
        self.move_player()
        self.draw_obstacles()
        self.move_obstacles()
        self.check_collisions()

    def move_player(self):
        """Função que define as características de movimentação do player
        """
        if self.__player.rect.center[0] < self.__fg_target_lane:
            self.__player.rect.x += self.__player._speed
            if self.__player.rect.center[0] > self.__fg_target_lane:
                self.__player.rect.center = (self.__fg_target_lane, self.__player.rect.centery)
        elif self.__player.rect.center[0] > self.__fg_target_lane:
            self.__player.rect.x -= self.__player._speed
            if self.__player.rect.center[0] < self.__fg_target_lane:
                self.__player.rect.center = (self.__fg_target_lane, self.__player.rect.centery)

    def draw_obstacles(self):
        """Função que desenha os obstáculos do jogo
        """
        if len(self.__obstacle_group) < 2:
            add_obstacle = True
            for obstacle in self.__obstacle_group:
                if obstacle.rect.top < obstacle.rect.height * 1.5:
                    add_obstacle = False

            if add_obstacle:
                lane = random.choice(lanes)
                image = random.choice(obstacle_images)
                obstacle = Obstacle(image, lane, screen_height / -2)
                self.__obstacle_group.add(obstacle)

    def move_obstacles(self):
        """Função que garante a movimentação dos obstáculos
        """
        for obstacle in self.__obstacle_group:
            obstacle.rect.y += self.__score._fg_speed
            if obstacle.rect.top >= screen_height:
                obstacle.kill()
                self.__score.update_score()

    def check_collisions(self):
        """Função que detecta colisões e realiza ações a respeito
        """
        if self.__collision_detection.check(self.__player, self.__obstacle_group):
            fg_collision_sound.play()
            self.__fg_gameover = True
            self.__player.set_dead()

    def render(self):
        """Função que renderiza o jogo
        """
        screen.fill((0, 0, 0))

        self.__background.draw_background(screen)

        if self.__player._visible:
            self.__player_group.draw(screen)

        self.__obstacle_group.draw(screen)

        self.__score.draw_score(screen)

        if self.__fg_gameover:
            screen.blit(death_box, (0, 0))

        pygame.display.update()

        while self.__fg_gameover:
            self.__clock.tick(100)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__fg_gameover = False

                if event.type == KEYDOWN:
                    if event.key == K_y:
                        self.reset_game()

                    elif event.key == K_n:
                        pygame.quit()
                        quit()

    def reset_game(self):
        """Função que define aspectos do jogo ao ser resetado
        """
        self.__fg_gameover = False
        self.__score._fg_speed = 2
        self.__score._fg_score = 0
        self.__obstacle_group.empty()
        self.__player.rect.center = [fg_player_x, fg_player_y]
        self.__player._visible = True
        self.__player.set_alive()

    pygame.display.set_caption('A Frog Journey')

if __name__ == "__main__":
    game = FrogJourneyGame()
    game.run()