import GameSimulator as g

from files import wordlist

def remove_complications(pattern, guess):
    out = ""
    for i in range(len(pattern)):
        if pattern[i] == "1":
            letter = guess[i]
            for j in range(len(guess)):
                if guess[i] == letter:
                     pattern[i] = "1"
    return pattern

print(remove_complications("21001", "seeds"))
