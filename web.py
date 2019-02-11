from flask import Flask
app = Flask(__name__)

from sudoku import *

@app.route("/")
def main():
    grid = Grid()
    return grid.html()

@app.route("/puzzle/<p>")
def load(p):
    grid = Grid("puzzles/" + p)
    return grid.html(p)

@app.route("/solve/<p>/<d>")
def s(p, d):
    grid = Grid("puzzles/" + p)
    solve(grid, int(d))
    return grid.html(p, int(d))
