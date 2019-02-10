n        = 9
minigrid = 3

import math

class Square:
    # A set<int> that stores the value(s) of the Square
    values = set()

    # __init__      initialize Square object
    # 
    # Inputs:
    #           n   size of grid (and number of possible values for Square)
    #           v   value of Square (if known). Set to None or ' ' if unknown
    #
    def __init__(self, n, v = None):
        if v is None or v is ' ':
            self.values = set(range(1,n+1))
        else:
            self.values = set([int(v)])
  

    # isSolved      return True if the Square is solved
    #
    def isSolved(self):
        return len(self.values) == 1


    # isUnsolved    Return true if the square is *completely* unsolved
    #
    def isUnsolved(self):
        return len(self.values) == n


    # reduce        Remove possible values we've ruled out
    #
    # Inputs:
    #           s   set<int> of values to rule out
    #
    # Returns:      True if we've solved the Square just now
    #
    def reduce(self, s):
        print("Values: {} ({}); Reductor: {} ({})".format(self.values, type(self.values), s, type(s)))
        self.values -= set(s)
        return self.isSolved()


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
            self._grid = [[Square(n, v) for v in list(line.strip("\n"))] for line in f]
        else:
            self._grid = [[Square(n) for i in range(0,n)] for j in range(0,n)]


    # html          Generate HTML representation of the sudoku grid
    #
    def html(self):
        h = '<link rel="stylesheet" type="text/css" href="/static/style.css">'
        h += "<table>\n"
        for i,row in enumerate(self._grid):
            h += "\t<tr>\n"
            for j,cell in enumerate(row):
                
                # Determine what border classes to apply
                classes = []
                if j == n - 1:
                    classes.append("right")
                elif j % minigrid == 0:
                    classes.append("left")
                
                if i % minigrid == 0:
                    classes.append("top")
                elif i == n - 1:
                    classes.append("bottom")

                (cellClass, cellValue) = cell.html()
                classes.append(cellClass)

                h += "\t\t<td class='{}'>{}</td>\n".format(' '.join(classes), cellValue)
            h += "\t</tr>\n"
        h += "</table>"
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
        i = math.floor(i/3)
        j = math.floor(j/3)
        l = [x[j*3:(j+1)*3] for x in self._grid[i*3:(i+1)*3]]
        return [i for x in l for i in x] # Flatten the list


    # isSolved      Find out if the entire puzzle is solved
    #
    # Returns:      True if the puzzle is solved. False otherwise
    #
    def isSolved(self):
        for i in range(0, n):
            for j in range(0, n):
                if _grid[i][j].isSolved() is False:
                    return False
        return True



# Given a 1D or 2D list of squares, create a set of all solved values in those squares
def getAllSolved(l):
    if type(l[0]) == list:
        return set([i for sub in l for i in sub if i.isSolved()])
    else:
        return set([i for i in l if i.isSolved()])


def solve(g):
    for i in range(0, n):
        for j in range(0, n):
            if g.get(i,j).isSolved():
                continue
            print("Solving ({},{})".format(i,j))
            
            r = getAllSolved(g.getRow(i,j))
            print("\tRemoving {} based on row".format(r))
            if g.reduce(i,j,r):
                print("\tSolved!")

            r = getAllSolved(g.getCol(i,j))
            print("\tRemoving {} based on col".format(r))
            if g.reduce(i,j,r):
                print("\tSolved!")
                
            r = getAllSolved(g.getSub(i,j))
            print("\tRemoving {} based on sub".format(r))
            if g.reduce(i,j,r):
                print("\tSolved!")

            print("\tNow: {}".format(g.get(i,j)))


