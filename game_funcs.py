import numpy as np
from peg import Peg

def initialize_board(t1, t2, t3, triangle_width, triangle_height, peg_radius):
    pegs = []
    for i in range(5):
        for j in range(i + 1):
            # switching to OOP
            x = t3[0] - (triangle_width / 10 * i - peg_radius) + (triangle_width / 5 * j - peg_radius)
            y = t3[1] + (triangle_height / 5 * (i) + peg_radius*2.4)
            in_play = 1
            row = i
            column = j
            peg = Peg(x, y, in_play, row, column)
            pegs.append(peg)
    return pegs


def pegs_in_play(pegs):
        count = 0
        for peg in pegs:
            if peg.in_play == 1:
                print(f"pegs in play: {peg.row} {peg.column}")
                count += 1
        return count


def valid_jump(p1, p2, pegs):
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
                y = valid_jump(peg, peg2, pegs)
                if valid_jump(peg, peg2, pegs):
                    possible_move = True
                    moves.append(y)
        for move in moves:
            print(move.row, move.column)
        print(f"Possible move? {possible_move}")
        return possible_move


def all_possible_moves(pegs):
        possible_move = False
        moves = []
        for peg in pegs:
            for peg2 in pegs:
                if peg == peg2:
                    continue
                if peg.in_play == 0:
                    continue
                if valid_jump(peg, peg2, pegs):
                    possible_move = True
                    moves.append(peg2)
        if possible_move:
            return moves
        return possible_move