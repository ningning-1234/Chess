import pygame
from tile import *
from settings import *
from game import *

run = True

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

game = ChessGame()
game.generate_board()

# todo
#  Figure out identical move notations
#  Save piece pos

while (run):
    events = pygame.event.get()
    mouse_events = {'pos':pygame.mouse.get_pos(), 'pressed':pygame.mouse.get_pressed()}
    for event in events:
        if event.type == pygame.QUIT:
            print('closing')
            game.save_fen()
            run = False

    game.update(events, mouse_events)

    #_____Draw_____
    window.fill(BG_COLOR)

    pygame.draw.rect(window, (0, 0, 0), pygame.Rect(58, 58, 484, 484))
    game.draw(window)

    pygame.display.flip()
    clock.tick(FPS)
