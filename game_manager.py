import pygame
import sys
import os
from board import Board
from constants import CUBE_SIZE, WIDTH, HEIGHT
from constants import BLACK, WHITE

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board(screen)
        self.started = False
        self.text = pygame.font.Font(f"{os.getcwd()}\\fonts\\arial.ttf", 30)

    def get_clicked(self):
        x, y = pygame.mouse.get_pos()
        x //= CUBE_SIZE
        y //= CUBE_SIZE
        return (y, x)

    def select(self, x, y):        
        self.board.select(x, y)

    def draw(self):
        if self.started:
            self.board.draw()
        else:
            self.draw_menu()

    def draw_menu(self):
        self.screen.fill(BLACK)
        text = self.text.render("Press any key to play", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - (text.get_width() // 2), HEIGHT // 2))

    def reset(self):
        self.__init__(self.screen)

    def quit(self):
        pygame.quit()
        sys.exit()

