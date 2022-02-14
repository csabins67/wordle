def loadFileAsArray(path):
    wordlist = []
    file = open(path, "r")
    for line in file:
        wordlist.append(line.strip())
    return wordlist

wordlist = loadFileAsArray("words.txt")
shortlist = loadFileAsArray("shortlist.txt")
