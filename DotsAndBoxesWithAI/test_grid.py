"""Test driver for the Grid class. Run it with: python test_grid.py"""
from grid import Grid


def check(description, actual, expected):
    """Print PASS if actual equals expected, otherwise print FAIL and both values."""
    if actual == expected:
        print(f"PASS: {description}")
    else:
        print(f"FAIL: {description} (expected {expected}, got {actual})")


grid = Grid(4)

check("Add a line between adjacent dots", grid.add_line((0, 0), (0, 1)), True)
check("Add the same line again", grid.add_line((0, 0), (0, 1)), False)
check("Add the same line in reverse", grid.add_line((0, 1), (0, 0)), False)
check("Add a diagonal line", grid.add_line((0, 0), (1, 1)), False)
check("Add a line to a dot that isn't adjacent", grid.add_line((0, 0), (0, 2)), False)
check("Add a line off the board", grid.add_line((0, 0), (0, -1)), False)
check("Only one line was added", len(grid.lines), 1)

print("\nThe grid should show one vertical line at the top left:")
grid.display()
