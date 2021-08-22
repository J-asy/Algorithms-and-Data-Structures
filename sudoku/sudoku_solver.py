""" Sudoku solver via backtracking """

from copy import deepcopy
import math


def get_subgrid_values(grid, row, col):
    """ Returns all values that belongs to the subgrid
    of the position specified by row and col in grid.
    """
    subgrid_size = int(math.sqrt(len(grid)))
    start_row = (row // subgrid_size)*subgrid_size
    start_col = (col // subgrid_size)*subgrid_size

    subgrid_val = []
    for i in range(start_row, start_row + subgrid_size):
        for j in range(start_col, start_col + subgrid_size):
            subgrid_val += [grid[i][j]]

    return subgrid_val


def valid_entry(grid, val, row, col):
    """ Returns true if filling the grid with the number val
    at the position specified by row and col gives a valid grid,
    otherwise returns false. """
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
    """ Given a partially filled grid, returns all possible grids
    with the number val fill in the specified row.
    """
    res = []
    if val in grid[row]:
        return [grid]
    for col in range(len(grid)):
        if valid_entry(grid, val, row, col):
            valid_grid = deepcopy(grid)
            valid_grid[row][col] = val
            res += [valid_grid]
    return res


def grids_augmented_with_number(part_grid, val, curr_row=0):
    """ Given a partially filled grid, returns all possible grids
    with the number val fill in to all of the rows.
    """
    if curr_row == len(part_grid):
        return [part_grid]
    else:
        res = []
        for option in grids_augmented_in_row(part_grid, val, curr_row):
            res += grids_augmented_with_number(option, val, curr_row + 1)
        return res


def solve(grid, num=1):
    """ Returns one possible solutions for the given grid """
    if num == len(grid) + 1:
        return grid, True
    else:
        for option in grids_augmented_with_number(grid, num):
            sol, flag = solve(option, num + 1)
            if flag:
                return sol, True
        return [], False


def sudoku_solver(filename):
    """ Reads the grid from a file, gets the solutions and displays them """
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    # format grid
    grid = []
    for line in lines:
        row = []
        for char in line.split(" "):
            row += [char if char == "x" else int(char)]
        grid.append(row)

    solution, flag = solve(grid)
    if flag:
        # display solution
        for row in solution:
            print(" " + str(row))
    else:
        print("Unsolvable")


if __name__ == "__main__":
    sudoku_solver("./sudoku/sudoku_testcase/a.txt")
