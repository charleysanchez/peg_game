import pygame
import numpy as np
from peg import Peg


def main():
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



    # pegs = dict()
    pegs = []
    for i in range(5):
        for j in range(i + 1):
            # peg[i, j] = x, y, has peg? (1 = yes, 0 = no), row, column
            # pegs[i, j] = [t3[0] - (triangle_width / 10 * i - peg_radius) + (triangle_width / 5 * j - peg_radius), t3[1] + (triangle_height / 5 * (i) + peg_radius*2.4), 1, i , j]
            # switching to OOP
            x = t3[0] - (triangle_width / 10 * i - peg_radius) + (triangle_width / 5 * j - peg_radius)
            y = t3[1] + (triangle_height / 5 * (i) + peg_radius*2.4)
            in_play = 1
            row = i
            column = j
            peg = Peg(x, y, in_play, row, column)
            pegs.append(peg)


    def valid_jump(p1, p2):
        if p2.in_play == 1:
            print("no hole to jump to")
            return False
        x_away = p2.row - p1.row
        y_away = p2.column - p1.column
        print(f"From: {p1.row}, {p1.column}")
        print(f"To: {p2.row}, {p2.column}")
        print(x_away)
        print(y_away)
        jumped_peg = (p1.row + x_away / 2, p1.column + y_away / 2)
        exists = False
        for peg in pegs:
            if (peg.row, peg.column) == jumped_peg:
                jumped_peg = peg
                exists = True
        
        if not exists:
            return False
        
        if (np.abs(x_away) != 2 and np.abs(y_away) != 2):
            print("not 2 away")
            return False


        if jumped_peg.in_play == 1:
            print(f"From: {p1.row}, {p1.column}")
            print(f"To: {p2.row}, {p2.column}")
            if np.abs(jumped_peg.row - p1.row) + np.abs(jumped_peg.column - p1.column) > 2:
                return False
            return jumped_peg
        else:
            return False

    def possible_move(pegs):
        possible_move = False
        moves = []
        for peg in pegs:
            for peg2 in pegs:
                if peg == peg2:
                    continue
                if peg.in_play == 0:
                    continue
                y = valid_jump(peg, peg2)
                if valid_jump(peg, peg2):
                    possible_move = True
                    moves.append(y)
        for move in moves:
            print(move.row, move.column)
        print(f"Possible move? {possible_move}")
        return possible_move

    def pegs_in_play():
        count = 0
        for peg in pegs:
            if peg.in_play == 1:
                print(f"pegs in play: {peg.row} {peg.column}")
                count += 1
        text = font.render(f'Game Over: {count} Pegs Left', True, "red", 'black')
        restart = font.render("press 'r' to restart", True, 'blue', 'black')
        restartRect = restart.get_rect()
        restartRect.topleft = (0, 0)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.blit(text, textRect)
        screen.blit(restart, restartRect)
        return count


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
                    main()
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
                    jumped_peg = valid_jump(selected, selected2)
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

        if not first and not possible_move(pegs):
            print("endgame")
            pegs_in_play()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
main()