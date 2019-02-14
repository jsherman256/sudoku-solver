from sudoku import Square
from sudoku import Grid
from sudoku import gridSize
from sudoku import miniGridSize

# ruleOutBasedOnKnowns  Reduce based on solved Squares in the same row/column/subgrid
#
# Inputs:
#           squares     list<Square>
#
# Returns:  True if we've reduced any possibilities
#
def ruleOutBasedOnKnowns(squares):
    productive = False

    knownValues = Square.getKnownValues(squares)
    for sq in squares:
        if sq.isSolved() is False:
            if sq.reduce(knownValues):
                productive = True

    return productive


# removeTwins           Given a list<Square>, remove any twins
#
# Inputs:
#           squares     list<Sqaure>
#
def removeTwins(squares):
    productive = False

    (twins, first, second) = Square.getTwins(squares)
    if twins is None:
        return

    print("Found {}".format(twins))
    for sq in squares:
        if sq is not first and sq is not second:
            if sq.reduce(twins):
                productive = True

    return productive


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
    productive = True
    r = 0
    
    # Iterate the grid as long as we're productive
    while productive:
        productive = False
        r += 1
        print("Round {}".format(r))

        for i in range(0, gridSize):
            if ruleOutBasedOnKnowns(g.getRow(i, 0)):
                productive = True
                print("\tReduced row {}".format(i))
            #removeTwins(g.getRow(i, 0))
            #singletons(g.getRow(i, 0))

        for j in range(0, gridSize):
            if ruleOutBasedOnKnowns(g.getCol(0, j)):
                productive = True
                print("\tReduced column {}".format(j))
            #removeTwins(g.getCol(0, j))
            #singletons(g.getCol(0, j))

        for a in range(0, miniGridSize):
            for b in range(0, miniGridSize):
                if ruleOutBasedOnKnowns(g.getSubByNum(a,b)):
                    productive = True
                    print("\tReduced subgrid {}".format((a,b)))
                #removeTwins(g.getSubByNum(a,b))
