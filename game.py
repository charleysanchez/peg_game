import pygame
import numpy as np
import game_funcs as gf
from peg import Peg
import random
import time


def main(ai=False):

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    width = screen.get_width()
    height = screen.get_height()

    board_color = (151, 92, 37)
    hole_color = tuple(component + 30 for component in board_color)
    background_color = (80, 200, 120)

    font = pygame.font.Font('freesansbold.ttf', 32)

    t1 = (width / 5, height * 4/5)
    t2 = (width * 4/5, height * 4/5)
    t3 = (width / 2, height / 5)

    triangle_height = t2[1] - t3[1]
    triangle_width = t2[0] - t1[0]

    peg_radius = 20
    selected = None
    selected2 = None
    first = True
    last_jumped_peg = None

    pegs = gf.initialize_board(t1, t2, t3, triangle_width, triangle_height, peg_radius)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("hi")
                x1, y1 = event.pos
                print(x1, y1)
                for p in pegs:
                    if x1 >= p.x - peg_radius and x1 <= p.x + peg_radius and y1 <= p.y + peg_radius and y1 >= p.y - peg_radius:
                        if selected is None:
                            selected = p
                        else:
                            selected2 = p
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main(ai)
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
                        


        screen.fill(background_color)
        pygame.draw.polygon(screen, board_color, (t1, t2, t3))
        for p in pegs:
            if p.in_play == 1:
                pygame.draw.circle(screen, "white", (p.x, p.y), peg_radius)
            else:
                pygame.draw.circle(screen, hole_color, (p.x, p.y), peg_radius/4)

        if selected:
            if not first and (selected.in_play) == 1:
                if selected2 is None:
                    pygame.draw.circle(screen, "red", (selected.x, selected.y), peg_radius - peg_radius/4)
                else:
                    jumped_peg = gf.valid_jump(selected, selected2, pegs)
                    last_jumped_peg = jumped_peg
                    if jumped_peg:
                        pygame.draw.circle(screen, board_color, (selected.x, selected.y), peg_radius)
                        pygame.draw.circle(screen, board_color, (jumped_peg.x, jumped_peg.y), peg_radius)
                        pygame.draw.circle(screen, "white", (selected2.x, selected2.y), peg_radius)

                        selected.in_play = 0
                        selected = None

                        jumped_peg.in_play = 0
                        jumped_peg = None

                        selected2.in_play = 1
                        selected2 = None
                        
                    else:
                        selected = None
                        selected2 = None

                    
            else:
                print(first)
                pygame.draw.circle(screen, board_color, (p.x, p.y), peg_radius)
                selected.in_play = 0
                first = False
                selected = None

        if not first and not gf.possible_move(pegs):
            print("endgame")
            count = gf.pegs_in_play(pegs)
            text = font.render(f'Game Over: {count} Pegs Left', True, "red", 'black')
            restart = font.render("press 'r' to restart", True, 'blue', 'black')
            restartRect = restart.get_rect()
            restartRect.topleft = (0, 0)
            textRect = text.get_rect()
            textRect.center = (width // 2, height // 2)
            screen.blit(text, textRect)
            screen.blit(restart, restartRect)
            if count != 1:
                main(ai)
        
        if ai:
            # time.sleep(1)
            if len(pegs) > 1:
                selected = pegs[random.randint(0, len(pegs) - 1)]
                while selected.in_play != 1:
                    selected = pegs[random.randint(0, len(pegs) - 1)]

                moves = gf.all_possible_moves(pegs)
                print(moves)
                if moves:
                    selected2 = moves[random.randint(0, len(moves) - 1)]
                    print((selected.row, selected.column), (selected2.row, selected2.column))

        pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()
main(ai=True)
