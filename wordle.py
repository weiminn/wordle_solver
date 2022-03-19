import json
from collections import OrderedDict

f = open('dictionary.json') 
data = json.load(f)
candidates = list(filter(lambda x: len(x) == 5 and '-' not in x and ' ' not in x, data))

alphabet = {
    'a': 0,
    'b': 0,
    'c': 0,
    'd': 0,
    'e': 0,
    'f': 0,
    'g': 0,
    'h': 0,
    'i': 0,
    'j': 0,
    'k': 0,
    'l': 0,
    'm': 0,
    'n': 0,
    'o': 0,
    'p': 0,
    'q': 0,
    'r': 0,
    's': 0,
    't': 0,
    'u': 0,
    'v': 0,
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0,
}

for candidate in candidates:
    for letter in candidate:
        alphabet[letter] = alphabet[letter] + 1

sortedAlphabet = OrderedDict(sorted(alphabet.items(), key=lambda x: x[1])) 

sortedAlphabetList = list(sortedAlphabet.keys())

k = 7 #choose the kth most used letters
mostUsed = set()
for i in range(k):
    mostUsed.add(sortedAlphabetList[len(sortedAlphabetList) - 1 - i])

extracted = []

for candidate in candidates:
    count = 0
    for letter in candidate:
        if letter in mostUsed:
            count = count + 1
    extracted.append([candidate, count])

sortedExtracted = list(sorted(extracted, key= lambda x: x[1]))

c = 100 #choose the cth most used words according to k most used letters
mostUsedWords = set()
for i in range(c):
    mostUsedWords.add(sortedExtracted[len(sortedExtracted) - 1 - i][0])

f.close()