from abstract import Minigame_abs
from settings import *
from endless_vertical_platformer import *
import sys

class DoodleJump(Minigame_abs):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.game_over = False
        self.jumpy = Jumper(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.enemy_sheet = SpriteSheet(enemy_sheet_image)
        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.scroll = 0
        self.background_scroll = 0
        self.game_over = False
        self.score = 0
        self.fade_counter = 0
        self.high_score = 0

    def create_background(self):
    # Atualiza a rolagem do plano de fundo com base no deslocamento (scroll)
        self.background_scroll += self.scroll

        # Desenha as imagens de fundo com base na rolagem
        self.screen.blit(background_image, (0, 0 + self.background_scroll))
        self.screen.blit(background_image, (0, -600 + self.background_scroll))

        # Verifica se a rolagem do plano de fundo ultrapassa o limite
        if self.background_scroll >= 600:
            # Reinicia a rolagem do plano de fundo
            self.background_scroll = 0
        

    def create_platforms(self):
        platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
        self.platform_group.add(platform)
        if len(self.platform_group) < MAX_PLATFORMS:
            platform_width = random.randint(40, 60)
            platform_x = random.randint(0, SCREEN_WIDTH - platform_width)
            platform_y = platform.rect.y - random.randint(80, 120)
            platform_type = random.randint(1, 2)
            if platform_type == 1 and self.score > 750:
                platform_movement = True
            else:
                platform_movement = False
            platform = Platform(platform_x, platform_y, platform_width, platform_movement)
            self.platform_group.add(platform)

    def draw_text(self, text, font, text_col, x, y):
        text_image = font.render(text, True, text_col)
        self.screen.blit(text_image, (x, y))
    
    def check_game_over(self):
        if self.jumpy.rect.top > SCREEN_HEIGHT:
            self.game_over = True
            death_sound.play()
        # Verificando se há colisão com inimigos
        if pygame.sprite.spritecollide(self.jumpy, self.enemy_group, False):
            if pygame.sprite.spritecollide(self.jumpy, self.enemy_group, False, pygame.sprite.collide_mask):
                self.game_over = True
                death_sound.play()

    def create_enemies(self):
        if len(self.enemy_group) == 0 and self.score > 1500:
            enemy = Enemy(SCREEN_WIDTH, 100, self.enemy_sheet, 1.5)
            self.enemy_group.add(enemy)

    def update_score(self):
        if self.scroll > 0:
            self.score += self.scroll


    def draw(self):
        # Desenhando uma linha da pontuação maior
        pygame.draw.line(self.screen, WHITE, (0, self.score - self.high_score + SCROLL_THRESH),
                         (SCREEN_WIDTH, self.score - self.high_score + SCROLL_THRESH), 3)
        self.draw_text("HIGH SCORE", font_small, WHITE, SCREEN_WIDTH - 130, self.score - self.high_score + SCROLL_THRESH)

        # Desenhando sprites do player
        self.platform_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.jumpy.draw()

        # Desenhando o painel
        pygame.draw.rect(self.screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
        pygame.draw.line(self.screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
        self.draw_text("SCORE: " + str(self.score), font_small, WHITE, 0, 0)

    def update(self):
        self.platform_group.update(self.scroll)
        self.enemy_group.update(self.scroll)

    def run(self):
        if not self.game_over:
            self.create_background()
            self.create_platforms()
            self.draw()
    
    

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game = DoodleJump(screen)


while True:
    # Configurando a taxa de atualização do jogo
    clock.tick(60)

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
    