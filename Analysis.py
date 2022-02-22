# This file is apart from the main program, intended to use the solver to calculate the best potential starting words
# beforehand, as calculating vast quantities of information beforehand and storing it in the name of efficiency seems to be
# a common theme here.
import Solver
from files import wordlist

#recursive function to calculate the best guesses of a list up to a specified depth. Not recommended past depth 3 (13000^3).
def find_best_recursive(solver, depth):
    if depth == 1:
        return solver.bestword
    else:
        out = []
        for i in range(243):
            lower_solver = Solver.Solver(solver.wordlist)
            lower_solver.next(solver.best_guess, i)
            out.append(find_best_recursive(lower_solver, depth - 1))
        return out

def level_two():
    for i in range(243):
        solver = Solver.Solver(wordlist)
        solver.next(solver.best_guess, i)
        yield solver.best_guess

#Solver.find_best(wordlist)

for guess in level_two():
    if guess == "":
        print("NONE")
    else:
        print(guess)
