import os
import sys
import pygame
from pygame.locals import *

# Constantes
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..")) # Diretorio do jogo
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
        pygame.image.load(f'{BASE_DIR}/assets/messages/splash.png'),
        pygame.image.load(f'{BASE_DIR}/assets/messages/pause.png')
    )
    SCENERY = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/border.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/corner.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/incorner.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/ground.png'), SCENERY_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/scenery/void.png'), SCENERY_SCALE)
    )
    SNAKE = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/head.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/body.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/curve.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/snake/tail.png'), ANIMALS_SCALE)
    )
    RABBIT = (
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm3.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm4.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm6.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm5.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm4.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm3.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm1.png'), ANIMALS_SCALE),
        pygame.transform.scale(pygame.image.load(f'{BASE_DIR}/assets/sprites/rabbit/frm2.png'), ANIMALS_SCALE)
    )
    BGM = (
        f'{BASE_DIR}/assets/sounds/bgm/main.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level1.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level2.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level3.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level4.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level5.mid'
    )
    sound_type = 'wav' if 'win' in sys.platform else 'ogg'           # Decisão do tipo de áudio
    FX = (
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/eat.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/die.{sound_type}')
    )
