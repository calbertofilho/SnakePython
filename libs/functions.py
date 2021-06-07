import sys
import time
from libs.settings import (
    MESSAGES, BGM, VOLUME_BGM
)
import pygame
from pygame.constants import (
    QUIT, KEYDOWN,
    K_ESCAPE, K_PAUSE,
)
from pygame.locals import *

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
