""" Sudoku solver via backtracking """

from copy import deepcopy
import math


def get_subgrid_values(grid, row, col):
    subgrid_size = int(math.sqrt(len(grid)))
    start_row = (row // subgrid_size)*subgrid_size
    start_col = (col // subgrid_size)*subgrid_size

    subgrid_val = []
    for i in range(start_row, start_row + subgrid_size):
        for j in range(start_col, start_col + subgrid_size):
            subgrid_val += [grid[i][j]]

    return subgrid_val


def valid_entry(grid, val, row, col):
    if grid[row][col] != 'x':
        return False

    # check subgrid
    if val in get_subgrid_values(grid, row, col):
        return False

    # check same row
    for c in grid[row]:
        if c == val:
            return False

    # check same col
    for r in range(len(grid)):
        if grid[r][col] == val:
            return False

    return True


def grids_augmented_in_row(grid, val, row):
    res = []
    if val in grid[row]:
        return [grid]
    for col in range(len(grid)):
        if valid_entry(grid, val, row, col):
            valid_grid = deepcopy(grid)
            valid_grid[row][col] = val
            res += [valid_grid]

    return res


# def grids_augmented_with_number(grid, val):
#     res = grids_augmented_in_row(grid, val, 0)

    # row = 1
    # while row < len(grid):
    #     for grid_ind in range(len(res)):
    #         res[grid_ind] = grids_augmented_in_row()

    # initialize
    # alter grids row by row
    # unfinised reject, finised correct

    # return res


def read_file(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    # retrieve grid
    grid = []
    for line in lines:
        row = []
        for char in line.split(" "):
            row += [char if char == "x" else int(char)]
        grid.append(row)
    return grid


def sudoku_solver(filename):
    grid = read_file(filename)
    # c = grids_augmented_with_number(grid, 1)
    # print(c)


if __name__ == "__main__":
    sudoku_solver("./sudoku_tests/b.txt")