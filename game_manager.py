import pygame
import sys
from board import Board
from constants import CUBE_SIZE

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(screen)

    def get_clicked(self):
        x, y = pygame.mouse.get_pos()
        x //= CUBE_SIZE
        y //= CUBE_SIZE
        return (y, x)

    def select(self, x, y):        
        self.board.select(x, y)

    def draw(self):
        self.board.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

