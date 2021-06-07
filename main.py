'''
Jogo da Cobrinha em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 04/06/2021
'''
# pylint: disable=no-member
# pylint: disable=no-name-in-module
# pylint: disable=c-extension-no-member
# pylint: disable=line-too-long

import os
import random
import sys
import time
import pygame
from pygame.constants import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_SPACE, K_PAUSE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT
)
#from pygame.locals import *

# Constantes
BASE_DIR = os.path.dirname(__file__)                                 # Diretorio do jogo
print(BASE_DIR)
VERSION = 'v2.0'                                                     # Versão do jogo
FPS = 15                                                             # Frames por segundo
BLOCKS = 20                                                          # Tamanho do bloco da matriz
ANIMALS_SCALE = (BLOCKS, BLOCKS)                                     # Escala criação dos animais
TILES = BLOCKS * 2                                                   # Tamanho das imagens tiles
SCENERY_SCALE = (TILES, TILES)                                       # Escala criação dos TileMaps
# Ativos
MESSAGES = None                                                      # Mensagens do jogo
SCENERY = None                                                       # TileMap do cenário
SNAKE = None                                                         # TileMap da cobra
RABBIT = None                                                        # Frames da animação do coelho
BGM = None                                                           # Músicas de fundo
FX = None                                                            # Efeitos
MAP = []                                                             # Mapa dos objetos da fase
# Definições de áudio
VOLUME_FX = 0.3                                                      # Volume dos efeitos especiais
VOLUME_BGM = 0.6                                                     # Volume da música de fundo
FADEOUT_BGM = 1500                                                   # Fade pra parar a música

class Screen():
    '''Classe que representa a tela do jogo'''
    def __init__(self):
        self.width = 800                                             # Comprimento da janela
        self.height = 600                                            # Altura da janela
        self.caption = f'SnakePython {VERSION}'                      # Título
        self.icon_location = f'{BASE_DIR}/res/images/icons/icon.png' # Local do ícone
        self.surface = pygame.display.set_mode((self.width, self.height)) # Criação da tela
        pygame.display.set_caption(self.caption)                     # Configuração do título
        self.icon = pygame.image.load(self.icon_location).convert_alpha() # Criação do ícone
        pygame.display.set_icon(self.icon)                           # Configuração do ícone
        os.environ['SDL_VIDEO_CENTERED'] = '1'                       # Centralização no desktop
    def update(self):
        '''Método que modela o comportamento da janela'''
        for event in pygame.event.get():                             # Identifica os eventos
            if event.type == QUIT:                                   # Evento: Fechar a janela
                close_game()                                         # Chamada da função de fechar
            if event.type == KEYDOWN:                                # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                            # Testa se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_PAUSE:                             # Testa se a tecla é "PAUSE"
                    pause_game(self, True)                           # Chamada da função de pausar
        pygame.display.update()                                      # Atualização de tela
    def get_surface(self):
        '''Método que retorna o painel de exibição dos objetos da janela'''
        return self.surface
    def get_size(self):
        '''Método que retorna o tamanho da tela'''
        return (self.width, self.height)

class Handycap(pygame.sprite.Sprite):
    '''Classe que representa o obstáculo no cenário'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 0
        self.length = 0
    def update(self):
        '''Método que representa o comportamento do obstáculo a cada iteração do jogo'''
    def set_position(self, pos_x, pos_y):
        '''Método que posiciona o obstáculo no cenário'''
        self.rect.x = pos_x
        self.rect.y = pos_y
    def get_position(self):
        '''Método que retorna a posição do obstáculo no cenário'''
        return self.rect
    def get_direction(self):
        '''Método que retorna a direção do obstáculo no cenário'''
        return self.direction
    def get_length(self):
        '''Método que retorna o comprimento do obstáculo no cenário'''
        return self.length

class Rabbit(pygame.sprite.Sprite):
    '''Classe que representa o coelho'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.current_image = 0
        self.image = RABBIT[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
    def update(self):
        '''Método que representa o comportamento do coelho a cada iteração do jogo'''
        self.current_image = (self.current_image + 1) % len(RABBIT)
        self.image = RABBIT[self.current_image]
        wait(0.1)
    def set_position(self, pos_x, pos_y):
        '''Método que posiciona o coelho na tela'''
        self.rect.x = pos_x
        self.rect.y = pos_y
    def get_position(self):
        '''Método que retorna a posição do coelho na tela'''
        return self.rect

class Snake(pygame.sprite.Sprite):
    '''Classe que representa a cobra'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = SNAKE[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.my_direction = 'Stop'
        self.body = [(0, 0), (0, BLOCKS), (0, (2 * BLOCKS))]
    def update(self):
        '''Método que representa o comportamento da cobra a cada iteração do jogo'''
    def set_initial_position(self, position):
        '''Método que seta a posição inicial da cobra na tela'''
        self.rect = position
    def set_direction(self, direction):
        '''Método que seta a direção da cabeça da cobra'''
        self.my_direction = direction
    def get_direction(self):
        '''Método que retorna a direção da cabeça da cobra'''
        return self.my_direction
    def grow_up(self):
        '''Método que cresce a cobra'''
        self.body.append((0, 0))

def init_libs(quality):
    '''Função que inicializa as biliotecas utilizadas no jogo'''
    if quality == 'high':                                            # Decisão da qualidade de som
        buf = 2048                                                   # Alta qualidade
    elif quality == 'mid':
        buf = 1024                                                   # Qualidade média
    else:
        buf = 512                                                    # Qualidade baixa
    pygame.init()                                                    # Inicialização do PyGame
    pygame.mixer.pre_init(                                           # Inicialização do áudio
        frequency = 44100,                                           # Frequência de 44100MHz
        size = -16,                                                  # Comprimento de onda 16bits
        channels = 2,                                                # Tocar em Stereo, 2 canais
        buffer = buf                                                 # Qualidade do som
    )

def populate_assets():
    '''Função que inicializa todos os ativos utilizados no jogo'''
    global MESSAGES, SCENERY, SNAKE, RABBIT, BGM, FX                 # Indica alteração na variável global
    MESSAGES = (
        pygame.image.load(f'{BASE_DIR}/res/images/messages/splash.png'),
        pygame.image.load(f'{BASE_DIR}/res/images/messages/pause.png')
    )
    SCENERY = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/scenery/border.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/scenery/corner.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/scenery/incorner.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/scenery/ground.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/scenery/void.png'), SCENERY_SCALE)
    )
    SNAKE = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/snake/head.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/snake/body.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/snake/curve.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/snake/tail.png'), ANIMALS_SCALE)
    )
    RABBIT = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm3.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm4.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm4.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm3.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/res/images/assets/rabbit/frm2.png'), ANIMALS_SCALE)
    )
    BGM = (
        f'{BASE_DIR}/res/sounds/bgm/main.mid',
        f'{BASE_DIR}/res/sounds/bgm/level1.mid',
        f'{BASE_DIR}/res/sounds/bgm/level2.mid',
        f'{BASE_DIR}/res/sounds/bgm/level3.mid',
        f'{BASE_DIR}/res/sounds/bgm/level4.mid',
        f'{BASE_DIR}/res/sounds/bgm/level5.mid'
    )
    sound_type = 'wav' if 'win' in sys.platform else 'ogg'           # Decisão do tipo de áudio
    FX = (
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/fx/{sound_type}/eat.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/fx/{sound_type}/die.{sound_type}')
    )

def get_scenery_tile(tilemap):
    '''Função que retorna as peças para a montagem do cenário'''
    scenery_tile = None
    if 'border_out' in tilemap:
        if 'top' in tilemap:
            scenery_tile = SCENERY[0]
        elif 'left' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[0], 90)
        elif 'bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[0], 180)
        elif 'right' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[0], 270)
    elif 'border_in' in tilemap:
        if 'top' in tilemap:
            scenery_tile = pygame.transform.flip(SCENERY[0], False, True)
        elif 'left' in tilemap:
            scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 90)
        elif 'bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 180)
        elif 'right' in tilemap:
            scenery_tile = pygame.transform.rotate(pygame.transform.flip(SCENERY[0], False, True), 270)
    elif 'corner_out' in tilemap:
        if 'left_top' in tilemap:
            scenery_tile = SCENERY[1]
        elif 'left_bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[1], 90)
        elif 'right_bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[1], 180)
        elif 'right_top' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[1], 270)
    elif 'corner_in' in tilemap:
        if 'left_top' in tilemap:
            scenery_tile = SCENERY[2]
        elif 'left_bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[2], 90)
        elif 'right_bottom' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[2], 180)
        elif 'right_top' in tilemap:
            scenery_tile = pygame.transform.rotate(SCENERY[2], 270)
    elif 'ground' in tilemap:
        scenery_tile = SCENERY[3]
    elif 'void' in tilemap:
        scenery_tile = SCENERY[4]
    return scenery_tile

def wait(delay):
    '''Função que atrasa a execução do código por um tempo determinado em segundos'''
    time_to_delay = time.time() + delay                              # Tempo inicial mais o delay
    while time.time() <= time_to_delay:                              # Enquanto não passar o delay
        pygame.display.update()                                      # Não faz nada

def play_bgm(track):
    '''Função para executar a música de fundo do jogo'''
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(BGM[track])                          # Carrega a música pra executar
        pygame.mixer.music.set_volume(VOLUME_BGM)                    # Configura o volume
        pygame.mixer.music.play(loops = -1)                          # Executa a música em loop

def pause_bgm(state):
    '''Função para suspender e resumir a música de fundo do jogo'''
    if pygame.mixer.music.get_busy():                                # Testa se há algo tocando
        if state is True:                                            # Se recebeu o valor True
            pygame.mixer.music.pause()                               # Pausa a execução
    else:                                                            # Se não há playback
        if state is False:                                           # Se recebeu o valor False
            pygame.mixer.music.unpause()                             # Retorna a execução

def stop_bgm(delay):
    '''Função para para a música de fundo do jogo'''
    pygame.mixer.music.fadeout(delay)                                # Executa o fadeout da música
    wait(delay / 1000)                                               # Transforma em segundos e espera
    pygame.mixer.music.stop()                                        # Para a execução da música

def pause_game(sface, state):
    '''Função que pausa o jogo'''
    pause_bgm(state)                                                 # Pausa a execução da música
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    while state:                                                     # Enquanto estiver pausado
        panel.blit(MESSAGES[1], (0, 0))                              # Exibe a mensagem de pause
        #panel.fill((0, 0, 0))                                        # Exibe uma tela preta
        for event in pygame.event.get():                             # Identifica os eventos
            if event.type == QUIT:                                   # Evento: Fechar a janela
                close_game()                                         # Chamada da função de fechar
            if event.type == KEYDOWN:                                # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                            # Teste se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_PAUSE:                             # Teste se a tecla é "PAUSE"
                    state = False                                    # Altera o estado e sai de PAUSE
                    pause_bgm(state)                                 # Reinicia a execução da música
        pygame.display.update()                                      # Atualização de tela

def close_game():
    '''Função que encerra o jogo'''
    pygame.quit()                                                    # Fecha a biblioteca PyGame
    pygame.mixer.quit()                                              # Encerra o reprodutor de aúdio
    sys.exit()                                                       # Encerra a execução

def show_matrix(sface, show_coordinates):
    '''Função que desenha na tela toda a matriz de obstáculos do jogo'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    size_x = sface.get_size()[0] // BLOCKS                           # Tamanho de colunas na matriz
    size_y = sface.get_size()[1] // BLOCKS                           # Tamanho de linhas na matriz
    sysfont = pygame.font.get_default_font()
    font = pygame.font.SysFont(sysfont, 14)
    for row in range(size_y):                                        # Para cada linha da matriz
        for column in range(size_x):                                 # Para cada coluna da matriz
            fill = -1 if MAP[row][column] == 1 else 1                # Representa a área de navegação
            pygame.draw.rect(                                        # Desenha o retângulo na posição
                panel,                                               # Painel de exibição do jogo
                (255, 0, 0),                                         # Cor: Verde
                (column * BLOCKS, row * BLOCKS, BLOCKS, BLOCKS),     # Posição na tela
                fill                                                 # Tipo de preenchimento
            )
            if show_coordinates is True:                             # Exibir posição de cada célula
                img = font.render(f'{row * BLOCKS}', True, (255, 255, 255)) # Define a linha
                panel.blit(img,
                                (column * BLOCKS,
                                row * BLOCKS)
                )                                                        # Exibe a posição da linha
                img = font.render(f'{column * BLOCKS}', True, (255, 255, 255)) # Define a coluna
                panel.blit(img,
                                ((column * BLOCKS) + (BLOCKS - img.get_width()),
                                (row * BLOCKS) + img.get_height())
                )                                                        # Exibe a posição da coluna

def create_base_stage(sface):
    '''Função que gera o mapa mais básico do jogo'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    # Desenho do terreno
    size_x = sface.get_size()[0] // TILES                            # Tamanho de colunas da tela
    size_y = sface.get_size()[1] // TILES                            # Tamanho de linhas da tela
    for column in range(size_x):                                     # Para cada coluna
        for row in range(size_y):                                    # Para cada linha
            panel.blit(get_scenery_tile('ground'), (column * TILES, row * TILES)) # Representação do chão
    # Desenho das cantos                                             # Representação dos cantos
    panel.blit(get_scenery_tile('corner_out_left_top'), (0, 0))      # Externo superior esquerdo
    panel.blit(get_scenery_tile('corner_out_left_bottom'), (0, 560)) # Externo inferior esquerdo
    panel.blit(get_scenery_tile('corner_out_right_top'), (760, 0))   # Externo superior direito
    panel.blit(get_scenery_tile('corner_out_right_bottom'), (760, 560)) # Externo inferior direito
    for row in range(TILES, sface.get_size()[0] - TILES, TILES):     # Representação das bordas
        panel.blit(get_scenery_tile('border_out_top'), (row, 0))     # Externa superior
        panel.blit(get_scenery_tile('border_out_bottom'), (row, 560)) # Externa inferior
    for column in range(TILES, sface.get_size()[1] - TILES, TILES):  # Representação das laterais
        panel.blit(get_scenery_tile('border_out_left'), (0, column)) # Lateral externa esquerda
        panel.blit(get_scenery_tile('border_out_right'), (760, column)) # Lateral externa direita
    # Criação da matriz com o mapa de navegação dos obstáculos
    # Representação do terreno, espaços vazios
    for row in range(size_y * 2):                                    # Representação do chão
        MAP.append([0] * (size_x * 2))                               # Preenchimento com zeros
    # Representação dos cantos
    MAP[0][0] = 1                                                    # Externo superior esquerdo
    MAP[580 // BLOCKS][0] = 1                                        # Externo inferior esquerdo
    MAP[0][780 // BLOCKS] = 1                                        # Externo superior direito
    MAP[580 // BLOCKS][780 // BLOCKS] = 1                            # Externo inferior direito
    for row in range(BLOCKS, sface.get_size()[0] - BLOCKS, BLOCKS):  # Representação das bordas
        MAP[0][row // BLOCKS] = 1                                    # Externa superior
        MAP[580 // BLOCKS][row // BLOCKS] = 1                        # Externa inferior
    for column in range(BLOCKS, sface.get_size()[1] - BLOCKS, BLOCKS): # Representação das laterais
        MAP[column // BLOCKS][0] = 1                                 # Lateral externa esquerda
        MAP[column // BLOCKS][780 // BLOCKS] = 1                     # Lateral externa direita

def create_obstacles(sface, num_obstacles):
    '''Função que gera os obstáculos da fase'''
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    # Criação dos obstáculos
    obstacles = []
    for qty in range(1, num_obstacles):
        length = random.randint(2, 10)
        direction = random.randint(0, 1)
        if direction == 0:
            position = (
                (random.randint(60, sface.get_size()[0] - 100 - (length * TILES)) // BLOCKS) * BLOCKS,
                (random.randint(60, sface.get_size()[1] - 100) // BLOCKS) * BLOCKS
            )
        if direction == 1:
            position = (
                (random.randint(60, sface.get_size()[0] - 100) // BLOCKS) * BLOCKS,
                (random.randint(60, sface.get_size()[1] - 100 - (length * TILES)) // BLOCKS) * BLOCKS
            )
        handicap = (position, length, direction)
        obstacles.insert(qty, handicap)
    print(num_obstacles - 1)
    # Desenho dos obstáculos
    for num, obstacle in enumerate(obstacles):
        position = obstacle[0]
        length = obstacle[1]
        direction = obstacle[2]
        if direction == 0:
            panel.blit(get_scenery_tile('corner_in_left_top'), position)
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (position[0], position[1] + TILES))
            for iterator in range(1, length + 1):
                panel.blit(get_scenery_tile('border_in_top'), (position[0] + (iterator * TILES), position[1]))
                panel.blit(get_scenery_tile('border_in_bottom'), (position[0] + (iterator * TILES), position[1] + TILES))
            panel.blit(get_scenery_tile('corner_in_right_top'), (position[0] + (iterator * TILES) + TILES, position[1]))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (position[0] + (iterator * TILES) + TILES, position[1] + TILES))
        if direction == 1:
            panel.blit(get_scenery_tile('corner_in_left_top'), position)
            panel.blit(get_scenery_tile('corner_in_right_top'), (position[0] + TILES, position[1]))
            for iterator in range(1, length + 1):
                panel.blit(get_scenery_tile('border_in_left'), (position[0], position[1] + (iterator * TILES)))
                panel.blit(get_scenery_tile('border_in_right'), (position[0] + TILES, position[1] + (iterator * TILES)))
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (position[0], position[1] + (iterator * TILES) + TILES))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (position[0] + TILES, position[1] + (iterator * TILES) + TILES))
        print(num, obstacle)
    # Adição dos obstáculos na matriz de navegação do jogo
    show_matrix(sface, True)                                         # Exibe a matriz na tela

def splash_screen(sface):
    '''Função que faz a animação da tela de abertura do jogo'''
    splash = True
    panel = sface.get_surface()                                      # Painel de exibição do jogo
    panel.blit(MESSAGES[0], (0, 0))                                  # Exibe a tela de apresentação do jogo
    while splash:
        for event in pygame.event.get():                             # Identifica os eventos
            if event.type == QUIT:                                   # Evento: Fechar a janela
                close_game()                                         # Chamada da função de fechar
            if event.type == KEYDOWN:                                # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                            # Testa se a tecla é "ESC"
                    close_game()                                     # Chamada da função de fechar
                if event.key == K_SPACE:                             # Testa se a tecla é "SPACE"
                    splash = False                                   # Encerra a tela de abertura
        pygame.display.update()                                      # Atualização de tela

def create_level(sface, stage):
    '''Função que gera os mapas dos níveis do jogo'''
    create_base_stage(sface)                                         # Cria o cenário básico
    play_bgm(stage)                                                  # Inicia a música de fundo
    if stage == 0:
        splash_screen(sface)                                  # Chama a tela de abertura
    elif stage <= 5:
        create_obstacles(sface, (stage + 1))                         # Cria o nível
    else:
        # Tela de créditos
        pass
    return stage <= 5

def set_rabbit_position(sface, prey):
    '''Função que posiciona o coelho na matriz'''
    pos_x = random.randint(BLOCKS, sface.get_size()[0] - BLOCKS)     # Gera uma posição aleatória pra 'X'
    pos_y = random.randint(BLOCKS, sface.get_size()[1] - BLOCKS)     # Gera uma posição aleatória pra 'Y'
    prey.set_position(pos_x // BLOCKS * BLOCKS, pos_y // BLOCKS * BLOCKS) # Coloca o coelho na posição

def main():
    '''Função principal que contempla a lógica de execução do jogo'''
    clock = pygame.time.Clock()                                      # Controle de tempo do jogo
    init_libs('low')                                                 # Inicialização dos recursos
    populate_assets()                                                # Carrega os ativos do jogo
    screen = Screen()                                                # Criação da janela
    predator_group = pygame.sprite.Group()
    snake = Snake()                                                  # Criação da cobra
    snake.set_initial_position((140, 280))
    predator_group.add(snake)
    prey_group = pygame.sprite.Group()
    rabbit = Rabbit()                                                # Criação do coelho
    prey_group.add(rabbit)
    create_level(screen, 0)                                          # Cria a tela de início do jogo
    stop_bgm(1500)                                                   # Para a música
    set_rabbit_position(screen, rabbit)                              # Posiciona o coelho para dar início ao jogo
    start = create_level(screen, 1)                                  # Dá início ao jogo
    while start:                                                     # Enquanto estiver em execução
        clock.tick(FPS)                                              # Configura o FPS do jogo
        commands = pygame.key.get_pressed()                          # Armazena os comandos do jogo
        if commands[K_UP]:                                           # Se pressionar a seta pra cima
            snake.set_direction('Up')                                # Indica que a cobra vai para cima
        if commands[K_DOWN]:                                         # Se pressionar a seta pra baixo
            snake.set_direction('Down')                              # Indica que a cobra vai para baixo
        if commands[K_LEFT]:                                         # Se pressionar a seta da esquerda
            snake.set_direction('Left')                              # Indica que a cobra vai para esquerda
        if commands[K_RIGHT]:                                        # Se pressionar a seta da direita
            snake.set_direction('Right')                             # Indica que a cobra vai para direita
        screen.update()                                              # Atualiza a tela
        snake.update()                                               # Atualiza a cobra
        rabbit.update()                                              # Atualiza o coelho
        predator_group.draw(screen.get_surface())                    # Atualiza a posição da cobra na tela
        prey_group.draw(screen.get_surface())                        # Atualiza a animação do coelho na tela
main()
try:                                                                 # Tenta executar
    while True:                                                      # Loop infinito
        main()                                                       # Dá início ao jogo
except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc: # Trata as exceções de erro
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")            # Feedback do que ocorreu
finally:                                                             # Finaliza
    close_game()                                                     # Chamada de saída do jogo
