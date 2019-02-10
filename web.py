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
    return grid.html()

@app.route("/solve/<p>")
def s(p):
    grid = Grid("puzzles/" + p)
    solve(grid)
    return grid.html()
