assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    twins = []
    for key_tmp, value_tmp in values.items():
        # build a list of tuples of twins boxes
        if len(value_tmp) == 2:
            twins += [sorted((key_tmp, peer)) for peer in peers[key_tmp] if values[peer] == value_tmp]        
    # eliminate identical tuples of twins
    twins_unique = set([tuple(twin) for twin in twins])
    # iterate twins
    for twins_unit in twins_unique:
        # iterate units and select the units contaning both twins from a tuple
        for unit_tmp in unitlist:
            if (twins_unit[0] in unit_tmp) and (twins_unit[1] in unit_tmp):
                for box_tmp in unit_tmp:
                    # remove digits from twins in the unit
                    if box_tmp not in twins_unit:
                        for digit in values[twins_unit[0]]:
                            values = assign_value(values, box_tmp, values[box_tmp].replace(digit, ''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    empty = '123456789'
    dic_grid = {}
    for box, val in zip(boxes, grid):
        if val == '.':
            dic_grid[box] = empty
        else:
            dic_grid[box] = val
    return dic_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers[key]:
                if value in values[peer]:
                    values = assign_value(values, peer, values[peer].replace(value, ''))
                    #values[peer] = values[peer].replace(value, '')   
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # TODO: Implement only choice strategy here
    for unit in unitlist:
        for digit in '123456789':
            box_places = [box for box in unit if digit in values[box]]
            if len(box_places) == 1:
                values = assign_value(values, box_places[0], digit)
                #values[box_places[0]] = digit
    return values

def reduce_puzzle(values):
    """
    This function receives as input an unsolved puzzle and applies three constraints 
    repeatedly in an attempt to solve it:
    - eliminate
    - only_choice
    - naked_twins
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        #print('Failed')
        return False 
    # Choose one of the unfilled squares with the fewest possibilities
    if all(len(values[s]) == 1 for s in boxes):
        #print('Solved')
        return values
    # use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    box = min(box for box in boxes if len(values[box]) > 1)
    #print(box)
    # use recurrence to solve each one of the resulting sudokus, and 
    for value in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #  Convert grid into a dictionary 
    values = grid_values(grid)
    # reduce puzzel using constrains
    values = reduce_puzzle(values) 
    # use depth-first search and propagation, create a search tree and solve the sudoku
    #values = search(values)
    return values

# define rows and columns
rows = 'ABCDEFGHI'
cols = '123456789'
# create a cross product of rows and cols for furture dictionary keys
boxes = cross(rows, cols)
# generate a lists of row, column, square, and diogonal units_
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[row_tmp[i]+cols[i] for i in range(9)] for row_tmp in (rows, rows[::-1])] 
# generate dictionaries of units and peers
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

