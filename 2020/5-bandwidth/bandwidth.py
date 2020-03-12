import math

# NOTE: This did *not* end up working in time for the end of the competition
# and is still in a non-working state.

# Some of the variable names don't follow the same names as in the brief:
#   This file           Brief
#   row                 i
#   column              j
#   count               k
#   rows                n
#   columns             m


def load_input(path):
    return [line.rstrip("\n") for line in open(path, "r")]


def save_output(path, l):
    path = path.replace("input", "output")
    open(path, "w").write("\n".join(l))

# Lambda function for splitting a list into chunks
comb = lambda s, n: (s[i:i+n] for i in range(0, len(s), n)) # noqa


def get_line(x1, y1, x2, y2):
    """Find the equation of a line in the form ax+by+c=0 from 2 points.

    Args:
        x1 (int): The first point's x coordinate.
        y1 (int): The first point's y coordinate.
        x2 (int): The second point's x coordinate.
        y2 (int): The second point's y coordinate.

    Returns:
        int, int, int: The a, b and c values for the line.
    """
    a = y1 - y2
    b = x2 - x1
    c = (x1 * y2) - (x2 * y1)
    return a, b, c


def dot_product(a, b, c, x0, y0):
    """Find the dot product of a point.

    This is used to find out how far away a point is from a line. The line
    needs to be in the format ax+by+c=0 and the point in the form (x, y).

    Args:
        a (int): The a value for the line.
        b (int): The b value for the line.
        c (int): The c value for the line.
        x0 (int): The x coordinate of the point.
        y0 (int): The y coordinate of the point.

    Returns:
        float: The distance from the line.
    """
    return (abs((a * x0) + (b * y0) + c)) / (math.sqrt((a ** 2) + (b ** 2)))


def point_distance(x1, y1, x2, y2):
    """Find the distance of two points.

    Args:
        x1 (int): The first point's x coordinate.
        y1 (int): The first point's x coordinate.
        x2 (int): The second point's x coordinate.
        y2 (int): The second point's y coordinate.

    Returns:
        float: The distance of between the points.
    """
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def is_vert(row, col):
    """Find out whether the row and column corresponds to a vertical or
    horizontal separation.

    Args:
        row (int): The row in the grid.
        col (int): The column in the grid.

    Returns:
        bool: True if the row and column is vertical or False if they are not.
    """
    a = 0 if row % 2 == 0 else 1
    b = col % 2 == a
    return b


def in_range(a, b, x):
    """Check if a value is within a specific range.

    Args:
        a (int): The start/end of the range.
        b (int): The start/end of the range.
        x (int): The value to be checked.

    Returns:
        bool: True if the value x is within the range, False if it is not.
    """
    # If a is biggest
    if a > b:
        if x >= b and x <= a:
            return True
    elif a < b:
        if x >= a and x <= b:
            return True
    return False


def exact_coords(row, col, count):
    """Get the 'exact' coordinates of a row and column depending on whether it
    it's third coorinate is 1 or 0.

    Returns:
        float, float: The exact coordinates of the square.
    """
    exact_row = row
    exact_col = col

    if is_vert(row, col):
        if count == 1:
            exact_row += 0.5
    else:
        if count == 1:
            exact_col += 0.5

    return exact_row, exact_col


def process(file):
    output = []
    lines = load_input(file)
    case_count = int(lines[0].strip())
    # Variable for the current line of the file that we are on. 1 is the
    # position of the first case
    case_line = 1

    for case_no in range(0, 1):
        print("========= CASE {} / {} ============".format(case_no + 1,
                                                           case_count))
        # The case information
        case_info = lines[case_line]
        rows = int(case_info.split(" ")[0])  # The number of rows in the 'grid'
        cols = int(case_info.split(" ")[1])  # The number of columns
        grid = [None] * rows  # Create an empty list of the length rows

        # Variables for storing the source and destination coordinates
        src_coords = None
        dest_coords = None

        # Create a grid from the case file
        for row in range(0, rows):
            # Get the row from the file, then split it into a list of chunks of
            # 2 (using comb), then convert that to a list and make each of the
            # strings inside that list be converted to a list (using map(list,
            # ...)) then convert the map to a list.
            data_row = list(map(list, list(comb(lines[case_line + 1 + row],
                                                2))))
            for col in range(0, cols):
                # If the source coordinate hasn't been found and S is in the
                # row
                if src_coords is None and "S" in data_row[col]:
                    src_coords = (row, col, data_row[col].index("S"))
                # If the destination coordiante hasn't been found and D is in
                # the row
                if dest_coords is None and "D" in data_row[col]:
                    dest_coords = (row, col, data_row[col].index("D"))

            # Set the grid's row to be the row that has been parsed from the
            # input
            grid[row] = data_row

        # Make sure that we have coordinates for the source and destination
        assert src_coords is not None
        assert dest_coords is not None

        # Calculate the exact coordinates for the source and destination
        src_coords_exact = exact_coords(*src_coords)
        dest_coords_exact = exact_coords(*dest_coords)

        # Find an equation of the line from source to destination in the form
        # ax + by + c = 0
        # This is called crow line from now on
        # AFTER COMPETITION NOTE: This *should* have used the exact coordinates
        a, b, c = get_line(src_coords[0], src_coords[1], dest_coords[0],
                           dest_coords[1])

        coords = []

        # For each of the coordinates on the grid, calculate the distance from
        # the crow line
        for row in range(0, rows):
            for col in range(0, cols):
                for count in range(0, 2):
                    # Don't add the source or destination coordinates to the
                    # list
                    if ((row, col) == src_coords[:2] or
                            (row, col) == dest_coords[:2]):
                        continue

                    # Get the grid item with the lowest value of the two
                    val = int(grid[row][col][count])

                    # If the smallest value is 9, it can't be upgraded
                    if val >= 9:
                        continue

                    # Get the exact coordinates of the grid position
                    exact_row, exact_col = exact_coords(row, col, count)

                    # If the coordinates are between the 2 points then
                    # calculate the dot product
                    if (in_range(src_coords[0], dest_coords[0], row) and
                            in_range(src_coords[1], dest_coords[1], col)):
                        print(("{} {} is inside range {} {} using dot "
                               "product").format(row, col, src_coords,
                                                 dest_coords))
                        dist = dot_product(a, b, c, exact_row, exact_col)
                    else:
                        print(("{} {} is outside range {} {} using point "
                               "distance").format(row, col, src_coords,
                                                  dest_coords))
                        # Calculate the distance of the point against both the
                        # source and destination coordinates
                        dist_a = point_distance(*src_coords_exact, exact_row,
                                                exact_col)
                        dist_b = point_distance(*dest_coords_exact, exact_row,
                                                exact_col)
                        # Get the smallest distance of the two
                        dist = dist_a if dist_a < dist_b else dist_b

                    coords.append([(row, col, count), dist, val])

        # Sort coordinates by the lowest distance from the crow line
        coords = sorted(coords, key=lambda x: (x[1], x[2]))
        print(coords)

    # Save the output to a file
    save_output(file, output)


process("input-ex.txt")
