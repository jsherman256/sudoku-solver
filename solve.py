from sudoku import Square
from sudoku import Grid
from sudoku import gridSize
from sudoku import miniGridSize

# ruleOutBasedOnKnowns  Reduce based on solved Squares in the same row/column/subgrid
#
# Inputs:
#               g       Grid to work on
#               i       Row index of Square to reduce
#               j       Column index of Square to reduce
#
# Returns:  True if we've just solved the Square
#
def ruleOutBasedOnKnowns(g, i, j):
    r = Square.getKnownValues(g.getRow(i,j))
    print("\tRemoving {} based on row".format(r))
    if g.reduce(i,j,r):
        return True

    r = Square.getKnownValues(g.getCol(i,j))
    print("\tRemoving {} based on col".format(r))
    if g.reduce(i,j,r):
        return True
        
    r = Square.getKnownValues(g.getSub(i,j))
    print("\tRemoving {} based on sub".format(r))
    if g.reduce(i,j,r):
        return True

    return False


# removeTwins           Given a list<Square>, remove any twins
#
# Inputs:
#           squares     list<Sqaure>
#
def removeTwins(squares):
    (twins, first, second) = Square.getTwins(squares)
    if twins is None:
        return

    print("Found {}".format(twins))
    for sq in squares:
        if sq is not first and sq is not second:
            sq.reduce(twins)


# singletons            If there's only one Square in the row that can take on a value,
#                       then that Square must have that value
#
# Inputs:
#           squares     list<Square>
#
def singletons(squares):
    # Count how many unsolved Squares could be each possibility
    freqs = {x: 0 for x in range(1, gridSize+1)}

    for sq in squares:
        if sq.isSolved() is False:
            for v in sq.values:
                freqs[v] += 1

    # Make list of singleton values found
    singles = [k for k,v in freqs.items() if v == 1]
    print(freqs)
    print("Found singletons: {}".format(singles))

    #for sq in squares:
    #    for s in singles: #TODO can this undo work we just did??
    #        if s in sq.values: 
    #            sq.set(s) #TODO this is broken for sure (causes duplicates and empties)


def solve(g, d):
    # Iterate the grid as many times as requested
    for x in range(0, d):
        # Check each cell
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                # Skip cells that are already solved
                if g.get(i,j).isSolved():
                    continue

                print("Solving ({},{})".format(i,j))
                
                # If we've just solved the cell, move on
                if ruleOutBasedOnKnowns(g, i,j) is True:
                    continue

        # Remove twins
        for i in range(0, gridSize):
            removeTwins(g.getRow(i, 0))
            singletons(g.getRow(i, 0))

        for j in range(0, gridSize):
            removeTwins(g.getCol(0, j))
            singletons(g.getCol(0, j))
