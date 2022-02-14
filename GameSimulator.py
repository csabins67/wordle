from Solver import Solver
from files import wordlist

class Game:
    def __init__(self, is_done_method, check_guess_method):
        self.is_done = is_done_method
        self.check_guess = check_guess_method

class Player:
    def __init__(self, get_feedback_method, give_feedback_method):
        self.get_feedback = get_feedback_method
        self.give_feedback = give_feedback_method

class Human_Player(Player):
    def __init__(self, use_solver):
        if use_solver:
            self.solver = Solver(wordlist)
        else:
            self.solver = None
        super().__init__(self.get_feedback, self.give_feedback)
        self.guess = None

    def get_feedback(self):
        if self.solver is not None:
            print("The solution bot thinks that " + self.solver.best_guess + " is the best answer.")
        self.guess = input("What is your guess? ")
        return self.guess

    def give_feedback(self, feedback):
        if self.solver is not None:
            self.solver.next(self.guess, feedback)
        import numpy as np
        ternary = np.base_repr(feedback, base=3)
        print("The game returned " + pad_left(ternary, 5, "0"))

#Pads the left size of a string sequence with element such that len(sequence) == size
def pad_left(sequence, size, element):
    return ("0" * (size - len(sequence))) + sequence

class AI(Player):
    def __init__(self):
        self.solver = Solver(wordlist)
        super().__init__(lambda : self.solver.best_guess,
                       lambda feedback : self.solver.next(self.solver.best_guess, feedback))

#Player inputs to the program the feedback from an actual game
class PCGame(Game):
    def __init__(self):
        super().__init__(self.is_done, self.check_guess)

    def is_done(self, times_checked):
        done_status = input("Enter Yes if done, No if not. ").upper()
        return done_status == "YES" or done_status == "Y"

    def check_guess(self, guess):
        pattern = input("Enter in returned pattern: 2 for grey, 1 for yellow, and 0 for green. ")
        return string_as_ternary(pattern)

def string_as_ternary(seq):
    total = 0
    for c in reversed(seq):
        total += int(c)
        total *= 3
    return total

#Computer simulation of game
class CCGame(Game):
    def __init__(self, secret):
        self.secret = secret
        self.done = False
        super().__init__(lambda times_checked : times_checked > 5 or self.done, self.check_guess)

    @classmethod
    def with_secret(cls, secret):
        return cls(secret)

    @classmethod
    def without_secret(cls):
        import random
        secret = random.choice(wordlist)
        return cls(secret)

    def check_guess(self, guess):
        from Matcher import match
        pattern = match(self.secret, guess)
        if pattern == 0:
            self.done = True
        return pattern

class Configuration:
    def __init__(self, Player, Game):
        self.player = Player
        self.game = Game
        self.times_checked = 0
    def run(self):
        while not self.game.is_done(self.times_checked):
            guess = self.player.get_feedback()
            feedback = self.game.check_guess(guess)
            self.times_checked += 1
            self.player.give_feedback(feedback)

def ProbeSimulation(secret):
    c = Configuration(AI(), CCGame.with_secret(secret))
    c.run()

def Practice():
    c = Configuration(Human_Player(True), CCGame.without_secret())
    c.run()

def Cheat():
    c = Configuration(Human_Player(True), PCGame())





