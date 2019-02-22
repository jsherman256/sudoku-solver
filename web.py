from flask import Flask
from flask import render_template
app = Flask(__name__)

from sudoku import *
from solve import solve

import os

@app.route("/puzzles/")
def listPuzzles():
    puzzles = os.listdir("puzzles")
    return render_template("list.html", puzzles = puzzles)

@app.route("/puzzle/<puzzle>")
@app.route("/solve/<puzzle>/<int:iterations>")
def load(puzzle, iterations = 0):
    grid = Grid("puzzles/" + puzzle)
    solve(grid, iterations)
    return render_template("puzzle.html", grid = grid, puzzle = puzzle, iterations = iterations)
