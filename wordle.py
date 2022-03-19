import json
from collections import OrderedDict
from numpy import random
import re

f = open('dictionary.json') 
data = json.load(f)
f.close()
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
    checked = set()
    for letter in candidate:
        if letter not in checked:
            alphabet[letter] = alphabet[letter] + 1

sortedAlphabet = OrderedDict(sorted(alphabet.items(), key=lambda x: x[1])) 

sortedAlphabetList = list(sortedAlphabet.keys())

k = 5 #choose the kth most used letters
mostUsedLetters = set()
for i in range(k):
    mostUsedLetters.add(sortedAlphabetList[len(sortedAlphabetList) - 1 - i])

extracted = []

for candidate in candidates:
    count = 0
    for letter in candidate:
        if letter in mostUsedLetters:
            count = count + 1
    extracted.append([candidate, count])

sortedExtracted = list(sorted(extracted, key= lambda x: x[1]))

c = 50 #choose the cth most used words according to k most used letters
mostUsedWords = list()
for i in range(c):
    mostUsedWords.append(sortedExtracted[len(sortedExtracted) - 1 - i][0])

#choose an answer key for testing
y_hat = random.choice(mostUsedWords, 1)[0]
mostUsedWords.remove(y_hat)
won = False

yellow_knowledge = set()
green_knowledge = ['', '', '', '', '']
foundGreen = False
triedWords = list()
# 5 tries in wordle

#first try use the most used words
firstTry = random.choice(mostUsedWords, 1)[0]
mostUsedWords.remove(firstTry)
triedWords.append(firstTry)
print("Try # 1:", firstTry)
input()

for l in range(len(firstTry)):
    if firstTry[l] is y_hat[l]:
        green_knowledge[l] = firstTry[l]
        foundGreen = True
    if firstTry[l] in y_hat:
        yellow_knowledge.add(firstTry[l])

print("Tried words:", triedWords)
print("Yellow Knowledge:", yellow_knowledge)
print("Green Knowledge:", green_knowledge)
print()

#second try onwards
for i in range(1, 5, 1):

    end = True
    for k in green_knowledge:
        if k is '':
            end = False
    if end:
        print("Congrats, the word is", ''.join(green_knowledge), '!!!')
        won = True
        break

    #narrow down according to knowledge
    wordsWithYellowSimilarity = {}
    for candidate in candidates:
        wordsWithYellowSimilarity[candidate] = len(set(candidate).intersection(yellow_knowledge))
    maximum = wordsWithYellowSimilarity[max(wordsWithYellowSimilarity, key=wordsWithYellowSimilarity.get)]
    yellowedCandidates = list(filter(lambda x: wordsWithYellowSimilarity[x] == maximum, wordsWithYellowSimilarity))

    greenedCandidates = yellowedCandidates

    if foundGreen:
        exp = ''
        for gL in green_knowledge:
            if gL is not '':
                exp = exp + gL
            else:
                exp = exp + '.'
        regex = re.compile(exp)
        greenedCandidates = [candidate for candidate in yellowedCandidates if re.match(regex, candidate)]

    #find the words with biggest difference in the narrowed space
    wordsWithDistance = {}
    for candidate in greenedCandidates:
        dist = 5
        checked = -1
        for l in range(len(candidate)):
            for tried in triedWords:
                if candidate[l] in tried and l is not checked:
                    dist = dist - 1
                    checked = checked + 1
            if l is not checked:
                checked = checked + 1
        wordsWithDistance[candidate] = dist
    maximum = wordsWithDistance[max(wordsWithDistance, key=wordsWithDistance.get)]
    candidates = list(filter(lambda x: wordsWithDistance[x] == maximum, wordsWithDistance))

    ithTry = random.choice(candidates, 1)[0]
    candidates.remove(ithTry)
    triedWords.append(ithTry)
    print("Try #", i + 1, ":", ithTry)
    input()

    #update knowledge
    for l in range(len(ithTry)):
        if ithTry[l] is y_hat[l]:
            green_knowledge[l] = ithTry[l]
            foundGreen = True
        if ithTry[l] in y_hat:
            yellow_knowledge.add(ithTry[l])

    print("Tried words:", triedWords)
    print("Yellow Knowledge:", yellow_knowledge)
    print("Green Knowledge:", green_knowledge)
    print()

    end = True
    for k in green_knowledge:
        if k is '':
            end = False
    if end:
        print("Congrats, the word is", ''.join(green_knowledge), '!!!')
        won = True
        break

if not won:
    print("Better luck next time!!!")
