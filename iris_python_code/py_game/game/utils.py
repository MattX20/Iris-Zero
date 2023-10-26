from random import shuffle
from numpy import intc


def generate_random_board():
    """This functions return random bit integers representing tuile colors on the board."""
    # 0 : yellow - black ; 1 : yellow - white ; 2 : red - black ; 3 : red - white ; 4 : yellow - red
    types = list(range(5))

    yellow_colors = 0
    red_colors = 0
    black_colors = 0
    white_colors = 0

    for c in range(4):
        shuffle(types)
        for i, k in enumerate(range(c * 5 + 1, (c + 1) * 5 + 1)):
            if types[i] == 0:
                yellow_colors += 1 << k
                black_colors += 1 << k
            elif types[i] == 1:
                yellow_colors += 1 << k
                white_colors += 1 << k
            elif types[i] == 2:
                red_colors += 1 << k
                black_colors += 1 << k
            elif types[i] == 3:
                red_colors += 1 << k
                white_colors += 1 << k
            else:
                yellow_colors += 1 << k
                red_colors += 1 << k

    return intc(yellow_colors), intc(red_colors), intc(black_colors), intc(white_colors)
