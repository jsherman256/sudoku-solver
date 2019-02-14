gridSize     = 9
miniGridSize = 3

import math

class Square:
    # A set<int> that stores the value(s) of the Square
    values = set()

    # __init__      initialize Square object
    # 
    # Inputs:
    #           gridSize   size of grid (and number of possible values for Square)
    #           v   value of Square (if known). Set to None or ' ' if unknown
    #
    def __init__(self, n, v = None):
        if v is None or v is ' ':
            self.values = set(range(1,n+1))
        else:
            self.values = set([int(v)])


    # set           Set value of Square
    #
    def set(self, v):
        self.values = set([v])
  

    # isSolved      return True if the Square is solved
    #
    def isSolved(self):
        return len(self.values) == 1


    # isUnsolved    Return true if the square is *completely* unsolved
    #
    def isUnsolved(self):
        return len(self.values) == gridSize


    # reduce        Remove possible values we've ruled out
    #
    # Inputs:
    #           s   set<int> of values to rule out
    #
    # Returns:      True if we've reduced any possibilties
    #
    def reduce(self, s):
        oldSet = self.values.copy()
        self.values -= set(s)
        return (oldSet != self.values)


    # html          Get info used for rendering Square as HTML
    #
    # Returns:      tuple(CSS class to use for display, value(s) to display)
    #           
    def html(self):
        if self.isSolved():
            return ('solved', str(list(self.values)[0]))
        elif self.isUnsolved():
            return ('','')
        else:
            return ('hints', ' '.join(str(x) for x in self.values))

   
    # getKnownValues    Given a list of Squares, create a set<int> of all solved values
    #
    # Inputs:
    #       squares     A list of Square objects
    #
    # Returns:          A set<int> of all solved values from the list of Squares provided
    #
    @staticmethod
    def getKnownValues(squares):
        knownValues = set([list(s.values)[0] for s in squares if s.isSolved()])
        return knownValues

    # getTwins          Given a list of Squares, find any twins (two cells with
    #                   identical pair possibilities (e.g. both can only be 4, 7)
    #
    # Inputs:
    #       squares     A list of Square objects
    #
    # Returns:          A thruple: (list<int> of twin values, first twin Sqaure,
    #                               second twin Sqaure)
    #
    #TODO this could be made to return ALL sets of twins
    #
    @staticmethod
    def getTwins(squares):
        for a,first in enumerate(squares):
            if len(first.values) == 2:
                for b,second in enumerate(squares[a+1:]):
                    if first.values == second.values:
                        return (list(first.values), first, second)

        return (None, None, None)


class Grid:
    # A 2D list of Square objects representing the sudoku grid
    _grid = None


    # __init__      Construct an empty grid or load a puzzle from a file
    #
    # Inputs:
    #       puzzle  Path to the text file of a puzzle to load
    #
    def __init__(self, puzzle = None):
        if puzzle:
            f = open(puzzle)
            self._grid = [[Square(gridSize, v) for v in list(line.strip("\n"))] for line in f]
        else:
            self._grid = [[Square(gridSize) for i in range(0,gridSize)] for j in range(0,gridSize)]


    # html          Generate HTML representation of the sudoku grid
    #
    def html(self, puzzle, solveCount = 0):
        h = '<link rel="stylesheet" type="text/css" href="/static/style.css">'
        h += "<table>\n"
        for i,row in enumerate(self._grid):
            h += "\t<tr>\n"
            for j,cell in enumerate(row):
                
                # Determine what border classes to apply
                classes = []
                if j == gridSize - 1:
                    classes.append("right")
                elif j % miniGridSize == 0:
                    classes.append("left")
                
                if i % miniGridSize == 0:
                    classes.append("top")
                elif i == gridSize - 1:
                    classes.append("bottom")

                (cellClass, cellValue) = cell.html()
                classes.append(cellClass)

                h += "\t\t<td class='{}'>{}</td>\n".format(' '.join(classes), cellValue)
            h += "\t</tr>\n"
        h += "</table>"
        h += "<br /><a href='{}'>Solve (more)</a>".format("/solve/{}/{}".format(puzzle, solveCount+1))
        return h


    # get           Get a reference to a Square object in the Grid
    #
    # Inputs:
    #           i   Row index
    #           j   Column index
    #
    # Returns:      reference to the requested Square object
    #
    def get(self, i, j):
        return self._grid[i][j]


    # reduce        Convenience function to reduce a specific Square object
    #
    # Inputs:
    #           i   Row index
    #           j   Column index
    #           s   set<int> of values to rule out from the Square
    #
    # Returns:      True if the Square is now solved
    #
    def reduce(self, i, j, s):
        return self._grid[i][j].reduce(s)


    # getRow        Get all Square objects in the same row as a given Square
    #
    # Inputs:
    #           i   Row index
    #           j   Column index
    #
    # Returns:      All Squares in the same row as (i,j) as a list
    # 
    def getRow(self, i, j):
        return self._grid[i]


    # getCol        Get all Square objects in the same column as a given Square
    #
    # Inputs:
    #           i   Row index
    #           j   Column index
    #
    # Returns:      All Squares in the same column as (i,j) as a list
    #
    def getCol(self, i, j):
        return [x[j] for x in self._grid]


    # getSubByNum   Get all Squares  given an x,y coord of the subgrid itself 
    #
    # Inputs:
    #           a   Subgrid row index
    #           b   Subgrid column index
    #
    # Returns:      All Squares from the selected subgrid
    #
    def getSubByNum(self, a, b):
        return self.getSub(a*miniGridSize, b*miniGridSize)


    # getSub        Get all Square objects in the same subgrid as a given Square
    #
    # Inputs:
    #           i   Row index
    #           j   Column index
    #
    # Returns:      All Squares in the same subgrid as (i,j) as a flattened list
    #
    # TODO make this independent of the puzzle size
    def getSub(self, i, j):
        i = math.floor(i/miniGridSize)
        j = math.floor(j/miniGridSize)
        l = [x[j*miniGridSize:(j+1)*miniGridSize] for x in self._grid[i*miniGridSize:(i+1)*miniGridSize]]
        return [i for x in l for i in x] # Flatten the list


    # isSolved      Find out if the entire puzzle is solved
    #
    # Returns:      True if the puzzle is solved. False otherwise
    #
    def isSolved(self):
        for i in range(0, gridSize):
            for j in range(0, gridSize):
                if _grid[i][j].isSolved() is False:
                    return False
        return True



