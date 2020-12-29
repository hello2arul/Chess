import pygame
import os
from game_manager import GameManager
from board import Board
from constants import WIDTH, HEIGHT

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load(f"{os.getcwd()}\images\\white_king.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = GameManager(screen)


while True:
    clock.tick(60)
    game.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = game.get_clicked()
            game.select(x, y)
        
        if event.type == pygame.KEYDOWN:
            game.started = True
            if event.key == pygame.K_r:
                game.reset()

    pygame.display.flip()


