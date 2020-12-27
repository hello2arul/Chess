import pygame
from game_manager import GameManager
from board import Board
from constants import WIDTH, HEIGHT

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_manager = GameManager(screen)


while True:
    clock.tick(60)
    game_manager.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_manager.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = game_manager.get_clicked()
            game_manager.select(x, y)

    pygame.display.flip()


