from __future__ import print_function
import sys
import os
import curses
from curses import wrapper
import time

def game_of_life(starting_state):
    current_state = starting_state
    while True:
        new_state = set()
        dead_cells = set()
        for cell in current_state:
            neighbours = get_neighbours(cell)
            dead_cells.update(neighbours - current_state)
            number_of_neighbours = len(neighbours & current_state)
            if number_of_neighbours > 1 and number_of_neighbours < 4:
                new_state.add(cell)
        for cell in dead_cells:
            neighbours = get_neighbours(cell)
            number_of_neighbours = len(neighbours & current_state)
            if number_of_neighbours == 3:
                new_state.add(cell)
        current_state = new_state
        yield current_state

def get_neighbours(cell):
    neighbour_offsets = {(-1, -1), (0, -1), (1, -1),
                         (-1, 0), (1, 0),
                         (-1, 1), (0, 1), (1, 1)}
    return {(cell[0] + offset[0], cell[1] + offset[1]) for offset in neighbour_offsets} 

def create_starting_set_of_cells(lines):
    starting_set = set()
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char == '-':
                starting_set.add((row, column))
    return starting_set

def write_state(screen, current_set, max_yx):
    screen.erase()
    for cell in current_set:
        if cell[0] < max_yx[0] and cell[0] >= 0 and cell[1] < max_yx[1] and cell[1] >= 0:
            screen.addch(cell[0], cell[1], '0')
    screen.refresh()

def begin(stdscr, starting_set):
    try:
        curses.curs_set(0)
        current_set = starting_set
        for next_set in game_of_life(current_set):
            max_yx = stdscr.getmaxyx()
            write_state(stdscr, current_set, max_yx)
            time.sleep(0.1)
            current_set = next_set
    except KeyboardInterrupt:
       curses.curs_set(2) 

def main(starting_file_name):
    if os.path.exists(starting_file_name):
        with open(starting_file_name, 'r') as starting_file:
            starting_file_lines = starting_file.readlines()
        for index, line in enumerate(starting_file_lines):
            if line[-1] == '\n':
                starting_file_lines[index] = line[:-1]
        starting_set = create_starting_set_of_cells(starting_file_lines)
        wrapper(begin, starting_set)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 game_of_life.py <starting_state_file>")
        sys.exit(1)
    main(sys.argv[1])
