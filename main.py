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

import random
import pygame
from pygame.constants import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_SPACE,
    K_UP, K_DOWN, K_LEFT, K_RIGHT
)
#from pygame.locals import *
from libs.functions import (
    close_game, play_bgm, stop_bgm
)
from libs.settings import (
    SCENERY, BLOCKS, TILES, MAP, MESSAGES, FPS,
    init_libs, populate_assets
)
from libs.Handycap import Handycap
from libs.Rabbit import Rabbit
from libs.Snake import Snake
from libs.Screen import Screen

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
