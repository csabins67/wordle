import math
from functools import reduce
from files import level2list
import Matcher

# This procedure calculates a table of the component-entropies of every frequency p(x) where 1/n <= x/n <= n/n, x is an integral,
# and n is the size of the sample space, in this case the number of words in the list, accounting for every possible event.
# (p(x) = 0 when no elements fall into a pattern, and p(x) = 1 when every element does.)
def make_entropy_table(n):
    table = [0] * n
    for probability in range(1, n):
        table[probability] = (entropy(probability, n))
    return table

#information entropy formula -p(x)*log(p(x))
def entropy(probability, total):
    return -(probability / total) * math.log(probability / total)

entropy_table = make_entropy_table(12972)

# The Solver class takes a list of words, and then progressively whittles that list down to one word based on the information a
# wordle game would give you.
class Solver:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.best_guess = "tares"#find_best(self.wordlist)

    def next(self, guess, resultant_pattern):
        self.wordlist = list(filter(lambda word: Matcher.match(word, guess) == resultant_pattern, self.wordlist))
        if guess == "tares":
            self.best_guess = level2list[resultant_pattern]
        else:
             self.best_guess = find_best(self.wordlist)


# To get maximum possible information from each guess, the information entropy of each word in the current wordlist is calculated.
# For each word, the frequency of every resulting match pattern from every other word are put into a list
# The entropy is then calculated with the help of the above table.
def find_best(wordlist):
    import numpy as np
    wordlist = np.asarray([[(ord(c) - 97) for c in word] for word in wordlist])
    tree = Matcher.make_word_tree(wordlist)
    best_word = ""
    best_total_entropy = 0

    def total_entropy(pattern_frequency_list):
        return reduce(lambda frq1, frq2: frq1 + entropy_table[frq2], pattern_frequency_list, 0)

    def entropies():
        for guess in wordlist:
            pattern_frequency_list = [0] * 5000
            for pattern in Matcher.get_match_list(guess, tree, len(wordlist)):
                pattern_frequency_list[pattern] += 1
            e = total_entropy(pattern_frequency_list)
            yield guess, e

    for guess, entropy, in entropies():
        if entropy > best_total_entropy:
            best_word = guess
            best_total_entropy = entropy
    return "".join([(chr(c+97)) for c in best_word])

def time_loop(sequence, n):
    import time
    last_time = time.process_time()
    c = 0
    for e in sequence:
        if c % n == 0:
            if c % (n*20) == 0:
                print(c)
            current_time = time.process_time()
            print(current_time - last_time)
            last_time = current_time
        c += 1
        yield e