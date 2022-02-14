import numpy as np

digits_green = [1<<2*i for i in range(0, 5)]
digits_yellow = [2 * (1<<2*i) for i in range(0, 5)]

# Singular match method to match two individual words. Constant time but somewhat inefficient. Returns number stored as
# genuine ternary as opposed to BCT.
def match(secret, guess):
    match_pattern = 0
    i = 0
    while i < 5:
        if guess[i] != secret[i]:
            j = 0
            while j < 5:
                if guess[i] == secret[j]:
                    match_pattern += 1
                    break
                elif j == 4:
                    match_pattern += 2
                j += 1
        match_pattern *= 3 #left shift match pattern
        i += 1
    return match_pattern // 3

#matches a guess word to a secret word, returning the pattern that would result from a wordle game
#For efficiency, the match pattern is computed as binary coded ternary.
#For each 2 binary digits, 00 is gray, 10 is yellow, and 01 is green, with 11 going unused
#The unused space is not missed, as using 32 bit ints is about 3 times as faster than other types anyway
#All we really need to do is generate a unique number for each possible match pattern, any representation will do
def get_match_list(word, wordtree, size):
    out = np.zeros(size, dtype=np.int32)

    for i in range(5):
        letter = word[i]
        for w in wordtree[letter]:
            out[w[0]] += digits_green[i]
            if letter == w[1][i]:
                out[w[0]] += digits_yellow[i]
    return out

def make_word_tree(wordlist):
    out = []
    for i in range(26):
        out.append([])
        for j in range(len(wordlist)):
            for c in wordlist[j]:
                if c == i:
                    out[i].append([j, wordlist[j]])
                    break
    return out
