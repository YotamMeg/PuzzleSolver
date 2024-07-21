#################################################################
# FILE : ex8.py
# WRITER : yotam megged , yotam267 , 319134912
# EXERCISE : intro2cs ex8 2022C
# DESCRIPTION: A program that solves a few puzzle problems using backtracking
# WEB PAGES I USED: stack over flow, programiz
#################################################################

from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]

Location = Tuple[int, int]
BLACK = 0
WHITE = 1
UNKNOWN = -1


def get_picture_scales(picture: Picture) -> Tuple[int, int]:
    """
    gets the height and width of a picture - number of rows and columns
    :param picture: a picture
    :return: a tuple
    """
    height = len(picture)
    width = len(picture[0])
    return height, width


def is_in_picture(rows: int, cols: int, location: Location) -> bool:
    """
    receives the number of rows and columns of a picture, and a location (row and col indexes), and checks if it is
    inside the picture
    :param rows: number of rows in the picture
    :param cols: number of columns in the picture
    :param location: a tuple containing a location
    :return: true if the location is inside the picture(including the edges), false if not
    """
    if location[0] < 0 or location[0] > rows - 1 or location[1] < 0 or location[1] > cols - 1:
        return False
    return True


def max_seen_rows(picture: Picture, row: int, col: int) -> int:
    """
    receives a picture, indexes for a location and checks how many cells in the current row can be seen
    from the current cell.
    :param picture: a picture
    :param row: the current row
    :param col: the current column
    :return: maximum number of cells seen in the same row
    """
    if picture[row][col] == BLACK:
        # then the cell doesn't see anything
        return 0
    height, width = get_picture_scales(picture)
    cell_counter = 1
    for i in range(col - 1, -1, -1):
        # first we check cells to the left of the given location
        if is_in_picture(height, width, (row, i)):
            # only check cells if they exist in the picture
            if picture[row][i] == BLACK:
                # then the cell won't see any further
                break
            else:
                cell_counter += 1
    for j in range(col + 1, width):
        if is_in_picture(height, width, (row, j)):
            if picture[row][j] == BLACK:
                break
            else:
                cell_counter += 1
    return cell_counter


def max_seen_cols(picture: Picture, row: int, col: int) -> int:
    """
    checks what is the maximum number of seen cells in the same column
    :param picture: a given picture
    :param row: the specific row
    :param col: the specific column
    :return: maximum number of seen cells in the same column
    """
    if picture[row][col] == BLACK:
        return 0
    height, width = get_picture_scales(picture)
    cell_counter = 1
    for i in range(row - 1, -1, -1):
        if is_in_picture(height, width, (i, col)):
            if picture[i][col] == BLACK:
                break
            else:
                cell_counter += 1
    for j in range(row + 1, height):
        if is_in_picture(height, width, (j, col)):
            if picture[j][col] == BLACK:
                break
            else:
                cell_counter += 1
    return cell_counter


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    returns the maximum number of seen cells, given a picture, and a location on it
    :param picture: a picture
    :param row: row index
    :param col: column index
    :return: the maximum cells seen from the given location
    """
    if picture[row][col] == BLACK:
        return 0
    return max_seen_rows(picture, row, col) + max_seen_cols(picture, row, col) - 1
    # we count the specific cell twice, so we need to return the sum minus 1


def min_seen_rows(picture: Picture, row: int, col: int) -> int:
    """
    finds the minimum number of seen cells on the same row given a picture and a location on it
    :param picture: a picture
    :param row: row index
    :param col: column index
    :return: the number of minimum seen cells
    """
    if picture[row][col] != WHITE:
        return 0
    height, width = get_picture_scales(picture)
    cell_counter = 1
    for i in range(col - 1, -1, -1):
        if is_in_picture(height, width, (row, i)):
            if picture[row][i] != WHITE:
                break
            else:
                cell_counter += 1
    for j in range(col + 1, width):
        if is_in_picture(height, width, (row, j)):
            if picture[row][j] != WHITE:
                break
            else:
                cell_counter += 1
    return cell_counter


def min_seen_cols(picture: Picture, row: int, col: int) -> int:
    """
    finds the minimum number of seen cells in the same column, given a picture and a location on it
    :param picture: a picture
    :param row: row index
    :param col: column index
    :return: the minimum number of seen cells in the same column from the given location
    """
    if picture[row][col] != WHITE:
        return 0
    height, width = get_picture_scales(picture)
    cell_counter = 1
    for i in range(row - 1, -1, -1):
        if is_in_picture(height, width, (i, col)):
            if picture[i][col] != WHITE:
                break
            else:
                cell_counter += 1
    for j in range(row + 1, height):
        if is_in_picture(height, width, (j, col)):
            if picture[j][col] != WHITE:
                break
            else:
                cell_counter += 1
    return cell_counter


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """
    returns the minimum number of seen cells in a picture, from a given location
    :param picture: a picture
    :param row: row index
    :param col: column index
    :return: the minimum number of seen cells
    """
    if picture[row][col] != WHITE:
        return 0
    return min_seen_rows(picture, row, col) + min_seen_cols(picture, row, col) - 1


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """
    receives a picture and a constraints set, and checks how successful can the constraints exist:
    if at least one of the constraints cannot happen, than we return 0
    else if all the constraints exist exactly - the minimum and the maximum seen cells are equal to the number
    in the constraints, we return 1
    else we return 2
    :param picture: a picture
    :param constraints_set: a set of constraints
    :return: 1, 2, or 3 representing the success rate of handling the constraints in the given picture
    """
    exact_solution = 0
    for constraint in constraints_set:
        if min_seen_cells(picture, constraint[0], constraint[1]) > constraint[2] or max_seen_cells(picture, constraint[0], constraint[1]) < constraint[2]:
            # a constraint cannot exist
            return 0
        elif min_seen_cells(picture, constraint[0], constraint[1]) == max_seen_cells(picture, constraint[0], constraint[1]) == constraint[2]:
            # a constraint exist exactly
            exact_solution += 1
    if exact_solution == len(constraints_set):
        # if all the constraints exist exactly
        return 1
    return 2


def get_close_cells(rows: int, cols: int, location: Location) -> List[Tuple]:
    """
    receives the number of rows and columns of a picture, and a location of a specific cell in the picture.
    it will return a list of all the cell's neighbouring cells, including itself
    :param rows: number of rows in the picture
    :param cols: number of columns in the picture
    :param location: a tuple
    :return: a list with 3-5 tuples containing all the required locations
    """
    list_of_cells = [location]
    for row in [location[0] - 1, location[0] + 1]:
        if is_in_picture(rows, cols, (row, location[1])):
            close_cell = row, location[1]
            list_of_cells.append(close_cell)
    for col in [location[1] - 1, location[1] + 1]:
        if is_in_picture(rows, cols, (location[0], col)):
            close_cell = location[0], col
            list_of_cells.append(close_cell)
    return list_of_cells


def init_puzzle(constraints_set: Set[Constraint], rows: int, cols: int) -> Picture:
    """
    creates the starting picture, if a cell should have no "visible" cells (the last value of the specific
    tuple in the set is 0) than the cell will get the value 0. the rest of the cells will get the value of -1 as we
    cannot determine their final value just yet
    :param cols: number of rows
    :param rows: number of columns
    :param constraints_set: a set of tuples containing all the given constraints
    :return: a picture with values of 0 and -1 in the required cells
    """
    new_picture = []
    for row in range(rows):
        new_row = []
        for col in range(cols):
            new_row.append(UNKNOWN)
        new_picture.append(new_row)
    for constraint in constraints_set:
        if constraint[2] == BLACK:
            new_picture[constraint[0]][constraint[1]] = BLACK
    return new_picture


def is_cell_legal(picture: Picture, constraints_set: Set[Constraint], location: Location) -> bool:
    """
    checks if a current status of a specific cell is legal - if the cell has no constraints, it"ll return true.
    if it has, it will check if the value of the constraint (the cell it needs to "see") is somewhere between the
    minimum and the maximum he actually sees. if it is, it will return true, if not, it'll return false.
    no need to check cells that are not in the constraint set because if all the cells from the set are legal,
    then the puzzle is solved
    :param picture: a picture
    :param constraints_set: set of constraints
    :param location: a tuple with row and col indexes
    :return: true if the status of the cell is legal, false if not
    """
    for constraint in constraints_set:
        index = constraint[0], constraint[1]
        if location == index:
            # we found a constraint for the cell
            break
    else:
        # we went over the constraints set and didn't find a constraint for the cell
        return True
    return min_seen_cells(picture, location[0], location[1]) <= constraint[2] <= max_seen_cells(picture, location[0], location[1])


def check_list_constraints(picture: Picture, constraints_set: Set[Constraint], cells_to_check: List[Tuple]) -> bool:
    """
    receives a picture, a set of constraints, and a list of cells to check, and checks if these cells meet the
    requirements of the matching constraint. a cell will meet the requirements and be "legal" if it is either not in
    the constraints set, or if it "sees" enough cells according to the constraint
    :param picture: a picture
    :param constraints_set: set of constraints
    :param cells_to_check: a list of tuples, each representing a location in the picture
    :return: true if all the cells in the list are legal, false otherwise
    """
    for cell in cells_to_check:
        if not is_cell_legal(picture, constraints_set, cell):
            return False
    return True


def get_relevant_cells(rows: int, cols: int, location: Location) -> List[Tuple]:
    """
    receives the number of rows and cols in a picture and a location, and returns a list with all the locations
    on the same row or column. it's necessary because when changing the value of a cell, we might interfere with other
    cells from the same row or column, so those are the cells we need to check
    :param rows: number of rows
    :param cols: number of columns
    :param location: a tuple representing a location
    :return: a list with the locations of all the cells in the same row and column
    """
    relevant_list = []
    for col in range(cols):
        relevant_location = location[0], col
        relevant_list.append(relevant_location)
    for row in range(rows):
        relevant_location = row, location[1]
        relevant_list.append(relevant_location)
    relevant_list.remove(location)
    # because we added the original location twice
    return relevant_list


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """
    solves a puzzle, after initializing it from the given number of rows, columns, and the constraints set.
    does so by calling the helper function recursively until it finds a solution or goes through all the options
    :param constraints_set: set of constraints
    :param n: number of rows
    :param m: number of columns
    :return: None if there is no solution to the puzzle, else will return the first solution it finds
    """
    picture = init_puzzle(constraints_set, n, m)
    if _solve_puzzle_helper(constraints_set, n, m, picture, 0):
        # if there is a solution
        return picture
    # there is no solution
    return


def _solve_puzzle_helper(constraints_set: Set[Constraint], rows: int, cols: int, picture: Picture, index) -> bool:
    """
    this function calls itself until it finds a solution, or until it finds that there are no solutions after checking
    all the options. each run it paints a cell - changes its value to 1, then checks all the other cells in the
    same row and columns to see if they meat the constraints. if they don't, it changes its value to 0. if they still
    don't meet the requirements it will change the cell value to -1 and return false. if they do it will call the
    function on the next index until it reaches the end, or until it finds that there are no solutions - in this case
    the function called on the first index will return the boolean value false
    :param constraints_set: a set of constraints
    :param rows: number of rows
    :param cols: number of columns
    :param picture: a picture
    :param index: an index
    :return: true if it finds a solution, false if not
    """
    if index == rows * cols:
        # we reached the end
        return True
    row, col = index // cols, index % cols
    # this formula gives us the correct row and col indexes
    if picture[row][col] != UNKNOWN:
        # if a cell is already painted, we move on to the next cell (because when we initialize
        # the picture we add the value 0 to certain cells if needed)
        return _solve_puzzle_helper(constraints_set, rows, cols, picture, index + 1)
    for color in [WHITE, BLACK]:
        picture[row][col] = color
        # paint the cell
        cells_to_check = get_relevant_cells(rows, cols, (row, col))
        # gets a list with the location of all the cells in the same row and col
        if not check_list_constraints(picture, constraints_set, cells_to_check):
            # if at least one of the cells now doesn't meat the constraints we add the value -1 to the cell
            # and try to put a different value if we haven't tried yet
            picture[row][col] = UNKNOWN
            continue
        if _solve_puzzle_helper(constraints_set, rows, cols, picture, index + 1):
            # if the function called on the next index returns true, it means it eventually reached the exit
            # condition (the first if) therefore we can return true
            return True
    picture[row][col] = UNKNOWN
    # change the value of a cell to -1 and return false, meaning in the current situation we didn't find a
    # solution, and we need to change the previous call
    return False


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """
    checks how many solutions a puzzle can have, given its sizes and a set of constraints. does so by calling
    the helper function recursively, until it goes through all the legal options for painting the cell. every time
    the helper function reaches the end of the picture, it will update the count of found solutions, and at the
    end it will return it
    :param constraints_set: a set of constraints
    :param n: number of rows
    :param m: number of columns
    :return: number of solutions found
    """
    starting_picture = init_puzzle(constraints_set, n, m)
    return _solution_counter_helper(constraints_set, n, m, starting_picture, 0, [0])


def _solution_counter_helper(constraints_set: Set[Constraint], rows: int, cols: int, picture: Picture, index, solution_counter: List[int]) -> int:
    """
    same as before, it calls itself until it reaches the last index, but this time if it does, it updates a counter.
    also, unlike before, when we call the function on the next index even if it returns true, we continue and not
    return true, which will ensure we will cover all the legal options. at the end, we simply return the counter
    :param constraints_set: a set of constraints
    :param rows: number of rows
    :param cols: number of columns
    :param picture: a picture
    :param index: a starting index
    :param solution_counter: a counter of solutions found
    :return: the number of solutions found
    """
    if index == rows * cols:
        solution_counter[0] += 1
        # update the counter
        return True
    row, col = index // cols, index % cols
    if picture[row][col] != UNKNOWN:
        # move to the next index
        return _solution_counter_helper(constraints_set, rows, cols, picture, index + 1, solution_counter)
    for color in [WHITE, BLACK]:
        picture[row][col] = color
        # paint the cell
        cells_to_check = get_relevant_cells(rows, cols, (row, col))
        if not check_list_constraints(picture, constraints_set, cells_to_check):
            picture[row][col] = UNKNOWN
            continue
        if _solution_counter_helper(constraints_set, rows, cols, picture, index + 1, solution_counter):
            # even if we get the return value true, we try the value 0 for the cell (if we haven't already), and
            # then put the value -1 to make sure we cover all the options
            continue
    picture[row][col] = UNKNOWN
    return solution_counter[0]
    # return the solution count


def is_cell_surrounded(picture: Picture, row, col) -> bool:
    """
    checks if a cell only has cells with value of 0 next to him, including itself
    :param picture: a given picture
    :param row: a row index
    :param col: a column index
    :return: true if the cell is surrounded with black cells (including itself), false otherwise
    """
    rows, cols = get_picture_scales(picture)
    close_cells = get_close_cells(rows, cols, (row, col))
    for cell in close_cells:
        if picture[cell[0]][cell[1]] != BLACK:
            return False
    return True


def init_max_set(picture: Picture) -> Set[Constraint]:
    """
    receives a final picture (with cells values of 0 and 1 only) and create a set of constraints with the maximum
    number of constraints - cells with value of 0, which all their neighboring cells also have the value 0, will get a
    constraint with value of 0 (and it will not change the entire game because its curtain). other cells with value of 0
    will get no constraints, and the rest will get a constraint with the value of the maximum cells they "see"
    :param picture: a picture with cells values of 0 and 1
    :return: a set of constraints which later will be optimized
    """
    ## only 0 should get black
    constraint_set = set()
    rows, cols = get_picture_scales(picture)
    for row in range(rows):
        for col in range(cols):
            if picture[row][col] != BLACK:
                max_value = max_seen_cells(picture, row, col)
                constraint_set.add((row, col, max_value))
            else:
                # the cell has value of 0 (black)
                if is_cell_surrounded(picture, row, col):
                    # then it is surrounded, and we add a constraint with value of 0
                    constraint_set.add((row, col, BLACK))
    return constraint_set


def copy_set(constraints_set: Set[Constraint]) -> Set[Constraint]:
    """
    receives a set and returns a copy of it
    :param constraints_set: a set of constraints
    :return: a copy of the original set
    """
    new_set = set()
    for constraint in constraints_set:
        new_set.add(constraint)
    return new_set


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    """
    receives a complete picture and creates a set of constraints that matches the requirements, by taking a constraint
    off each time, and checking if the number of solutions is still 1. if it's not one it will add the constraint
    back and move to the next constraint
    :param picture: a given picture
    :return: the final set of constraints
    """
    rows, cols = get_picture_scales(picture)
    max_set = init_max_set(picture)
    final_set = copy_set(max_set)
    for constraint in max_set:
        final_set.remove(constraint)
        if how_many_solutions(final_set, rows, cols) == 1:
            # move to the next constraint
            continue
        # if we took off a wrong constraint then we put it back
        final_set.add(constraint)
    return final_set
