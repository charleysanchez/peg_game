import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
width = screen.get_width()
height = screen.get_height()

board_color = (151, 92, 37)
hole_color = tuple(component + 30 for component in board_color)
background_color = (80, 200, 120)

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



pegs = dict()
for i in range(5):
    for j in range(i + 1):
        # peg[i, j] = x, y, has peg? (1 = yes, 0 = no), row, column
        pegs[i, j] = [t3[0] - (triangle_width / 10 * i - peg_radius) + (triangle_width / 5 * j - peg_radius), t3[1] + (triangle_height / 5 * (i) + peg_radius*2.4), 1, i , j]


def valid_jump(p1, p2):
    if pegs[p2][2] == 1:
        print("no peg to jump")
        return False
    x_away = (pegs[p2][3] - pegs[p1][3])
    y_away = (pegs[p2][4] - pegs[p1][4])
    print(x_away)
    print(y_away)
    jumped_peg = p1[0] + x_away / 2, p1[1] + y_away / 2
    if (np.abs(x_away) != 2 and np.abs(y_away) != 2):
        print("not 2 away")
        return False
    # handle horizontal movement
    if np.abs(x_away) == 2 and y_away == 0:
        if pegs[jumped_peg][2] == 1:
            return jumped_peg
    # handle "vertical" movement
    elif np.abs(x_away) == 0 and np.abs(y_away) == 2:
        if pegs[jumped_peg] == 1:
            return jumped_peg
    elif np.abs(x_away) == 2 and np.abs(y_away) == 2:
        print(jumped_peg)
        if pegs[jumped_peg] == 1:
            return jumped_peg


print(pegs)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("hi")
            x1, y1 = event.pos
            print(x1, y1)
            for p in pegs.keys():
                if x1 >= pegs[p][0] - peg_radius / 2 and x1 <= pegs[p][0] + peg_radius / 2 and y1 <= pegs[p][1] + peg_radius / 2 and y1 >= pegs[p][1] - peg_radius / 2:
                    if selected is None:
                        selected = p
                    else:
                        selected2 = p
                    

    screen.fill(background_color)
    pygame.draw.polygon(screen, board_color, (t1, t2, t3))
    for p in pegs.keys():
        if pegs[p][2] == 1:
            pygame.draw.circle(screen, "white", pegs[p][:2], peg_radius)
        else:
            pygame.draw.circle(screen, hole_color, pegs[p][:2], peg_radius/4)
    # print(selected, selected2, last_jumped_peg)
    if selected:
        if not first and pegs[selected][2] == 1:
            if selected2 is None:
                pygame.draw.circle(screen, "red", pegs[selected][:2], peg_radius - peg_radius/4)
            else:
                jumped_peg = valid_jump(selected, selected2)
                last_jumped_peg = jumped_peg
                if jumped_peg:
                    pygame.draw.circle(screen, board_color, pegs[selected][:2], peg_radius)
                    pygame.draw.circle(screen, board_color, pegs[jumped_peg][:2], peg_radius)
                    pygame.draw.circle(screen, "white", pegs[selected2][:2], peg_radius)

                    pegs[selected][2] = 0
                    selected = None

                    pegs[jumped_peg][2] = 0
                    jumped_peg = None

                    pegs[selected2][2] = 1
                    selected2 = None
                    
                else:
                    selected = None
                    selected2 = None


                
        else:
            print(first)
            pygame.draw.circle(screen, board_color, pegs[selected][:2], peg_radius)
            pegs[selected][2] = 0
            print(pegs.keys())
            first = False
            selected = None


    pygame.display.flip()

    clock.tick(60)

pygame.quit()