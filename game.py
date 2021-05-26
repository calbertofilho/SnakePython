'''
Jogo da Cobrinha em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 25/05/2021
'''
# pylint: disable=no-member
# pylint: disable=no-name-in-module

import os
import random
import sys
import pygame
from pygame.constants import (
    QUIT, KEYDOWN, K_ESCAPE, K_SPACE
    #K_PAUSE, K_UP, K_DOWN, K_LEFT, K_RIGHT
)
#from pygame.locals import *

# Constantes
BASE_DIR = os.path.dirname(__file__)                                  # Diretorio do jogo
VERSION = 'v1.0'                                                      # Versão do jogo
FPS = 15                                                              # Frames por segundo
BLOCKS = 20
BORDER = BLOCKS * 2


class Screen():
    '''Classe que representa a tela do jogo'''
    def __init__(self):
        self.width = 800                                              # Comprimento da janela
        self.height = 600                                             # Altura da janela
        self.caption = f'SnakePython {VERSION}'                       # Título
        self.icon_location = f'{BASE_DIR}/assets/icons/icon.png'      # Local do ícone
        self.surface = pygame.display.set_mode((self.width, self.height)) # Criação da tela
        pygame.display.set_caption(self.caption)                      # Configuração do título
        self.icon = pygame.image.load(self.icon_location).convert_alpha() # Criação do ícone
        pygame.display.set_icon(self.icon)                            # Configuração do ícone
        os.environ['SDL_VIDEO_CENTERED'] = '1'                        # Centralização no desktop

    def update(self):
        '''Método que modela o comportamento da janela'''
        for event in pygame.event.get():                              # Controle de eventos
            if event.type == QUIT:                                    # Evento: Fechar a janela
                close_game()
            if event.type == KEYDOWN:                                 # Evento: Pressionar tecla
                if event.key == K_ESCAPE:                             # Teste se a tecla é "ESC"
                    close_game()
        pygame.display.update()                                       # Atualização de tela

    def get_surface(self):
        '''Método que retorna o painel de exibição dos objetos da janela'''
        return self.surface

    def get_size(self):
        '''Método que retorna o tamanho da tela'''
        return (self.width, self.height)

class Snake(pygame.sprite.Sprite):
    '''Classe que representa a cobra'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        '''Método que representa o comportamento da cobra a cada iteração do jogo'''
    def get_direction(self):
        '''Método que retorna a direção da cabeça da cobra'''

class Rabbit(pygame.sprite.Sprite):
    '''Classe que representa o coelho'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        '''Método que representa o comportamento do coelho a cada iteração do jogo'''

def init_libs():
    '''Função que inicializa as biliotecas utilizadas no jogo'''
    pygame.init()                                                     # Inicialização do PyGame
    pygame.mixer.pre_init(                                            # Inicialização do áudio
        frequency = 44100, size = 16, channels = 1, buffer = 512
    )

def get_scenery_tile(tilemap):
    '''Função que retorna as peças para a montagem do cenário'''
    scale = (BORDER, BORDER)
    scenery = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/border.png'), scale),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/corner.png'), scale),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/incorner.png'), scale),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/ground.png'), scale),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/void.png'), scale)
    )
    scenery_tile = None
    if 'border' in tilemap:
        if 'out' in tilemap:
            if 'top' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[0], 0)
            if 'left' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[0], 90)
            if 'bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[0], 180)
            if 'right' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[0], 270)
        if 'in' in tilemap:
            if 'top' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(scenery[0], False, True), 0)
            if 'left' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(scenery[0], False, True), 90)
            if 'bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(scenery[0], False, True), 180)
            if 'right' in tilemap:
                scenery_tile = pygame.transform.rotate(pygame.transform.flip(scenery[0], False, True), 270)
    if 'corner' in tilemap:
        if 'out' in tilemap:
            if 'left_top' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[1], 0)
            if 'left_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[1], 90)
            if 'right_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[1], 180)
            if 'right_top' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[1], 270)
        if 'in' in tilemap:
            if 'left_top' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[2], 0)
            if 'left_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[2], 90)
            if 'right_bottom' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[2], 180)
            if 'right_top' in tilemap:
                scenery_tile = pygame.transform.rotate(scenery[2], 270)
    if 'ground' in tilemap:
        scenery_tile = pygame.transform.rotate(scenery[3], 0)
    if 'void' in tilemap:
        scenery_tile = pygame.transform.rotate(scenery[4], 0)
    return scenery_tile

def create_base_stage(sface):
    '''Função que gera o mapa mais básico do jogo'''
    panel = sface.get_surface()                                       # Painel de exibição do jogo
    # Desenho do terreno
    size_x = sface.get_size()[0] // BORDER
    size_y = sface.get_size()[1] // BORDER
    for line in range(size_x):
        if (size_x - 1) > line >= 1:
            for column in range(size_y):
                if (size_y - 1) > column >= 1:
                    panel.blit(get_scenery_tile('ground'), (line * BORDER, column * BORDER))
    # Desenho das bordas
    panel.blit(get_scenery_tile('corner_out_left_top'), (0, 0))
    panel.blit(get_scenery_tile('corner_out_left_bottom'), (0, 560))
    panel.blit(get_scenery_tile('corner_out_right_top'), (760, 0))
    panel.blit(get_scenery_tile('corner_out_right_bottom'), (760, 560))
    for line in range(BORDER, sface.get_size()[0] - BORDER, BORDER):
        panel.blit(get_scenery_tile('border_out_top'), (line, 0))
        panel.blit(get_scenery_tile('border_out_bottom'), (line, 560))
    for column in range(BORDER, sface.get_size()[1] - BORDER, BORDER):
        panel.blit(get_scenery_tile('border_out_left'), (0, column))
        panel.blit(get_scenery_tile('border_out_right'), (760, column))

def create_obstacles(sface, num_obstacles):
    '''Função que gera os obstáculos da fase'''
    panel = sface.get_surface()                                       # Painel de exibição do jogo
    # Criação dos obstáculos
    obstacles = []
    for qty in range(1, num_obstacles):
        size = random.randint(2, 10)
        direction = random.randint(0, 1)
        if direction == 0:
            position = (
                (random.randint(60, sface.get_size()[0] - 100 - (size * BORDER)) // 10) * 10,
                (random.randint(60, sface.get_size()[1] - 100) // 10) * 10
            )
        if direction == 1:
            position = (
                (random.randint(60, sface.get_size()[0] - 100) // 10) * 10,
                (random.randint(60, sface.get_size()[1] - 100 - (size * BORDER)) // 10) * 10
            )
        handicap = (position, size, direction)
        obstacles.insert(qty, handicap)
    # Desenho dos obstáculos
    for num, obstacle in enumerate(obstacles):
        if obstacle[2] == 0:
            panel.blit(get_scenery_tile('corner_in_left_top'), obstacle[0])
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (obstacle[0][0], obstacle[0][1] + BORDER))
            for iterator in range(1, obstacle[1] + 1):
                panel.blit(get_scenery_tile('border_in_top'), (obstacle[0][0] + (iterator * BORDER), obstacle[0][1]))
                panel.blit(get_scenery_tile('border_in_bottom'), (obstacle[0][0] + (iterator * BORDER), obstacle[0][1] + BORDER))
            panel.blit(get_scenery_tile('corner_in_right_top'), (obstacle[0][0] + (iterator * BORDER) + BORDER, obstacle[0][1]))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (obstacle[0][0] + (iterator * BORDER) + BORDER, obstacle[0][1] + BORDER))
        if obstacle[2] == 1:
            panel.blit(get_scenery_tile('corner_in_left_top'), obstacle[0])
            panel.blit(get_scenery_tile('corner_in_right_top'), (obstacle[0][0] + BORDER, obstacle[0][1]))
            for iterator in range(1, obstacle[1] + 1):
                panel.blit(get_scenery_tile('border_in_left'), (obstacle[0][0], obstacle[0][1] + (iterator * BORDER)))
                panel.blit(get_scenery_tile('border_in_right'), (obstacle[0][0] + BORDER, obstacle[0][1] + (iterator * BORDER)))
            panel.blit(get_scenery_tile('corner_in_left_bottom'), (obstacle[0][0], obstacle[0][1] + (iterator * BORDER) + BORDER))
            panel.blit(get_scenery_tile('corner_in_right_bottom'), (obstacle[0][0] + BORDER, obstacle[0][1] + (iterator * BORDER) + BORDER))
        print(num, obstacle)
    # Criação da matriz de navegação do jogo
    size_x = sface.get_size()[0] // BLOCKS
    size_y = sface.get_size()[1] // BLOCKS
    for line in range(size_x):
        if (size_x - 1) > line >= 1:
            for column in range(size_y):
                if (size_y - 1) > column >= 1:
                    pygame.draw.rect(
                        panel,
                        (255, 0, 0),
                        (line * BLOCKS, column * BLOCKS, BLOCKS, BLOCKS),
                        1
                    )

def create_level(sface, stage):
    '''Função que gera os mapas dos níveis do jogo'''
    create_base_stage(sface)
    if stage == 0:                                                    # Define a Tela de início
        create_obstacles(sface, random.randint(2, 6))

def close_game():
    '''Função que encerra o jogo'''
    pygame.quit()
    sys.exit()

def main():
    '''Função principal que contempla a lógica de execução do jogo'''
    init_libs()                                                       # Inicialização dos recursos
    screen = Screen()                                                 # Criação da janela
    sound_type = 'wav' if 'win' in sys.platform else 'ogg'            # Decisão do tipo de áudio
    clock = pygame.time.Clock()                                       # Controle de tempo do jogo
    level = 0                                                         # Configura pra tela de início
    create_level(screen, level)                                       # Cria a tela selecionada
    start = True                                                      # Dá início a execução do jogo

    while start:
        clock.tick(FPS)
        screen.update()
        commands = pygame.key.get_pressed()
        if commands[K_SPACE]:
            start = False

try:
    while True:
        main()
except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")
finally:
    close_game()
