import sys
import pygame

class Snake(pygame.sprite.Sprite):
    '''Classe que representa a cobra'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        pass

class Apple(pygame.sprite.Sprite):
    '''Classe que representa a maçã'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        pass

def main():
    pass

try:
    while True:
        main()
except (ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")
finally:
    pygame.quit()
    sys.exit()
