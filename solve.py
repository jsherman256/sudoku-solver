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
    print("\tFound singletons: {}".format(singles))

    for sq in squares:
        for s in singles: #TODO can this undo work we just did??
            if s in sq.values: 
                print("\tSetting {} to {}".format(sq.values, s))
                sq.set(s) #TODO this is broken for sure (causes duplicates and empties)


def solverApply(g, func, rows = True, cols = True, subs = True):
    productive = True

    while productive:
        productive = False
        if rows:
            for i in range(0, gridSize):
                print("Row {}".format(i))
                if func(g.getRow(i, 0)):
                    productive = True

        if cols:
            for j in range(0, gridSize):
                print("Column {}".format(j))
                if func(g.getCol(0, j)):
                    productive = True

        if subs:
            for a in range(0, miniGridSize):
                for b in range(0, miniGridSize):
                    print("Subgrid {},{}".format(a,b))
                    if func(g.getSubByNum(a,b)):
                        productive = True



def solve(g, d):
    sequence = [ruleOutBasedOnKnowns, removeTwins, ruleOutBasedOnKnowns, singletons, ruleOutBasedOnKnowns, singletons, ruleOutBasedOnKnowns, singletons ] * 5
    rs       = [True,                 True,         True,                True,       True,                 False,      True,                 False] * 5 
    cs       = [True,                 True,         True,                False,      True,                 True,       True,                 False] * 5
    ss       = [True,                 True,         True,                False,      True,                 False,      True,                 True] * 5

    for i in range(0, d):
        solverApply(g, sequence[i], rs[i], cs[i], ss[i])
